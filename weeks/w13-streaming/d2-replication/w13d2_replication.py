"""W13 D2: one partition replicated on n brokers: ISR, high watermark, acks, failover."""


class NotEnoughReplicas(Exception):
    pass


class PartitionOffline(Exception):
    pass


class Partition:
    def __init__(self, n_replicas: int = 3, min_insync: int = 2, unclean: bool = False):
        self.logs: dict[int, list] = {i: [] for i in range(n_replicas)}   # replica id -> list of values
        self.alive: set[int] = set(range(n_replicas))
        self.isr: set[int] = set(range(n_replicas))
        self.leader: int | None = 0
        self.hw = 0
        self.epoch = 0
        self.min_insync, self.unclean = min_insync, unclean

    def _advance_hw(self) -> None:
        """HW = min LEO over the ISR. During normal operation it never moves backwards."""
        # TODO
        raise NotImplementedError

    def produce(self, value, acks) -> int:
        """Append to the leader's log, return the offset. acks is 0, 1 or "all".
        No leader -> PartitionOffline. acks == "all" with len(ISR) < min_insync -> NotEnoughReplicas
        (nothing is appended). Then update the HW."""
        # TODO
        raise NotImplementedError

    def acked(self, offset: int, acks) -> bool:
        """Has the producer of `offset` received its acknowledgement?
        acks 0 or 1: as soon as the leader has the record. "all": only once offset < HW."""
        # TODO
        raise NotImplementedError

    def replicate(self, follower: int, max_records: int | None = None) -> None:
        """One fetch by an alive follower (ignore the call if it is dead, is the leader, or there is no leader).
        1. Truncate the follower's log to its longest common prefix with the leader's log.
        2. Copy up to max_records of the leader's following records (None = all).
        3. If the follower's LEO now equals the leader's, add it to the ISR. Update the HW."""
        # TODO
        raise NotImplementedError

    def shrink_isr(self, follower: int) -> None:
        """The leader drops a lagging follower from the ISR (never itself). Update the HW."""
        # TODO
        raise NotImplementedError

    def fetch(self, offset: int, max_records: int = 100) -> list:
        """Consumer read from the leader: only records below the HW."""
        # TODO
        raise NotImplementedError

    def fail(self, replica: int) -> None:
        """Broker crash: remove from alive and ISR (its log stays on disk). If it was the leader, elect:
        the lowest-id alive ISR member; if the ISR is empty: with unclean=True the lowest-id alive replica
        (the ISR becomes {that replica}), otherwise no leader (None). On a new leader: epoch += 1 and
        HW = min(HW, new leader's LEO) (it only drops after an unclean election)."""
        # TODO
        raise NotImplementedError

    def recover(self, replica: int) -> None:
        """Broker restart: alive again, NOT in the ISR until a replicate() catches it up. If the partition
        had no leader and this replica was the last ISR member... keep it simple: if there is no leader and
        unclean=True, it becomes leader (ISR = {replica}, epoch += 1, HW = min(HW, its LEO))."""
        # TODO
        raise NotImplementedError
