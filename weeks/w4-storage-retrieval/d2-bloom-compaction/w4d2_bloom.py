"""W4 D2: Bloom filter and LSM compaction (k-way merge, newest version wins)."""
import hashlib
import heapq
import math

TOMBSTONE = "__tombstone__"


def optimal_params(n: int, p: float) -> tuple:
    """(m bits, k hashes) for n keys at false-positive rate p. m = ceil, k = max(1, round)."""
    m = math.ceil(-n * math.log(p) / (math.log(2) ** 2))
    k = max(1, round(m / n * math.log(2)))
    return m, k


def false_positive_rate(m: int, n: int, k: int) -> float:
    return (1 - math.exp(-k * n / m)) ** k


class BloomFilter:
    def __init__(self, m: int, k: int):
        self.m, self.k = m, k
        self.bits = bytearray((m + 7) // 8)

    def _positions(self, item: str) -> list:
        """k positions via double hashing: h1, h2 = two 64-bit halves of sha256(item); pos_i = (h1 + i*h2) % m."""
        d = hashlib.sha256(item.encode()).digest()
        h1 = int.from_bytes(d[:8], "big")
        h2 = int.from_bytes(d[8:16], "big") | 1
        return [(h1 + i * h2) % self.m for i in range(self.k)]

    def add(self, item: str) -> None:
        for p in self._positions(item):
            self.bits[p >> 3] |= 1 << (p & 7)

    def might_contain(self, item: str) -> bool:
        return all(self.bits[p >> 3] & (1 << (p & 7)) for p in self._positions(item))


def compact(runs: list, drop_tombstones: bool) -> list:
    """runs: newest first; each run is a sorted list of (key, value), keys unique within a run.
    Return one sorted run with the newest value per key; drop keys whose newest value is TOMBSTONE
    if drop_tombstones, else keep the tombstone entry."""
    tagged = [[(k, age, v) for k, v in run] for age, run in enumerate(runs)]
    out, last = [], None
    for k, age, v in heapq.merge(*tagged):
        if k == last:
            continue  # an older version of a key already emitted (smaller age = newer sorts first)
        last = k
        if v == TOMBSTONE and drop_tombstones:
            continue
        out.append((k, v))
    return out
