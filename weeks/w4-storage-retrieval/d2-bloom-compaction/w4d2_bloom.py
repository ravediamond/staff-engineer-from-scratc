"""W4 D2: Bloom filter and LSM compaction (k-way merge, newest version wins)."""
import hashlib
import heapq
import math

TOMBSTONE = "__tombstone__"


def optimal_params(n: int, p: float) -> tuple:
    """(m bits, k hashes) for n keys at false-positive rate p. m = ceil, k = max(1, round)."""
    # TODO
    raise NotImplementedError


def false_positive_rate(m: int, n: int, k: int) -> float:
    # TODO
    raise NotImplementedError


class BloomFilter:
    def __init__(self, m: int, k: int):
        self.m, self.k = m, k
        self.bits = bytearray((m + 7) // 8)

    def _positions(self, item: str) -> list:
        """k positions via double hashing: h1, h2 = two 64-bit halves of sha256(item); pos_i = (h1 + i*h2) % m."""
        # TODO
        raise NotImplementedError

    def add(self, item: str) -> None:
        # TODO
        raise NotImplementedError

    def might_contain(self, item: str) -> bool:
        # TODO
        raise NotImplementedError


def compact(runs: list, drop_tombstones: bool) -> list:
    """runs: newest first; each run is a sorted list of (key, value), keys unique within a run.
    Return one sorted run with the newest value per key; drop keys whose newest value is TOMBSTONE
    if drop_tombstones, else keep the tombstone entry."""
    # TODO
    raise NotImplementedError
