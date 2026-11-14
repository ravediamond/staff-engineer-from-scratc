"""W13 D3: partitioner, idempotent producer, range assignor, group coordinator with generations."""
import zlib


def partition_for(key: str, n_partitions: int) -> int:
    """Stable partitioner: zlib.crc32 of the UTF-8 key, modulo n_partitions.
    (Python's hash() is salted per process: never use it for anything that must agree across machines.)"""
    return zlib.crc32(key.encode("utf-8")) % n_partitions


def moved_fraction(keys: list[str], n_old: int, n_new: int) -> float:
    """Fraction of keys whose partition changes when the topic goes from n_old to n_new partitions."""
    return sum(partition_for(k, n_old) != partition_for(k, n_new) for k in keys) / len(keys)


class OutOfOrderSequence(Exception):
    pass


class IdempotentBroker:
    """One partition. Deduplicates retries with (producer id, sequence number)."""

    def __init__(self):
        self.log: list = []
        self.last: dict[int, tuple[int, int]] = {}   # pid -> (last accepted seq, its offset)

    def append(self, pid: int, seq: int, value) -> tuple[str, int]:
        """A producer's first record has seq 0.
        seq == last + 1 -> append, return ("ok", offset).
        seq == last     -> do not append, return ("duplicate", offset of the original).
        anything else   -> raise OutOfOrderSequence."""
        last_seq, last_off = self.last.get(pid, (-1, -1))
        if seq == last_seq + 1:
            self.log.append(value)
            self.last[pid] = (seq, len(self.log) - 1)
            return "ok", len(self.log) - 1
        if seq == last_seq and last_seq >= 0:
            return "duplicate", last_off
        raise OutOfOrderSequence(f"pid {pid}: got seq {seq}, expected {last_seq + 1}")


def range_assign(members: list[str], n_partitions: int) -> dict[str, list[int]]:
    """Range assignor: sort the members; each gets a contiguous block of n // m partitions, and the first
    n % m members get one more. Every partition is assigned exactly once."""
    members = sorted(members)
    base, extra = divmod(n_partitions, len(members))
    out, start = {}, 0
    for i, m in enumerate(members):
        size = base + (1 if i < extra else 0)
        out[m] = list(range(start, start + size))
        start += size
    return out


class StaleGeneration(Exception):
    pass


class GroupCoordinator:
    def __init__(self, n_partitions: int):
        self.n_partitions = n_partitions
        self.members: set[str] = set()
        self.generation = 0
        self.assignment: dict[str, list[int]] = {}
        self.committed: dict[int, int] = {}      # partition -> next offset to read

    def _rebalance(self) -> None:
        """Provided: new generation, new assignment."""
        self.generation += 1
        self.assignment = range_assign(sorted(self.members), self.n_partitions) if self.members else {}

    def join(self, member: str) -> int:
        """Add the member, rebalance, return the new generation."""
        self.members.add(member)
        self._rebalance()
        return self.generation

    def leave(self, member: str) -> None:
        """Remove the member (session timeout or clean shutdown) and rebalance."""
        self.members.discard(member)
        self._rebalance()

    def commit(self, member: str, generation: int, partition: int, offset: int) -> None:
        """Store the committed offset. Raise StaleGeneration unless the generation is the current one AND the
        member currently owns the partition (a zombie from before a rebalance must not move offsets)."""
        if generation != self.generation or partition not in self.assignment.get(member, []):
            raise StaleGeneration(f"{member} gen {generation} (current {self.generation}) partition {partition}")
        self.committed[partition] = offset

    def lag(self, end_offsets: dict[int, int]) -> dict[int, int]:
        """Per partition: log end offset - committed offset (0 if never committed)."""
        return {p: end - self.committed.get(p, 0) for p, end in end_offsets.items()}
