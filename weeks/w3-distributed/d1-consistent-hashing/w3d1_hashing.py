"""W3 D1: consistent hashing ring with virtual nodes, and rendezvous hashing."""
import bisect
import hashlib
from collections import Counter


def stable_hash(s: str) -> int:
    """Deterministic across processes: first 8 bytes of MD5, big-endian."""
    return int.from_bytes(hashlib.md5(s.encode()).digest()[:8], "big")


class Ring:
    def __init__(self, vnodes: int = 100):
        self.vnodes = vnodes
        self.points: list = []   # sorted hashes
        self.owner: dict = {}    # hash -> node

    def add(self, node: str) -> None:
        """Insert `vnodes` points named f"{node}#{i}"."""
        for i in range(self.vnodes):
            p = stable_hash(f"{node}#{i}")
            bisect.insort(self.points, p)
            self.owner[p] = node

    def remove(self, node: str) -> None:
        for i in range(self.vnodes):
            p = stable_hash(f"{node}#{i}")
            j = bisect.bisect_left(self.points, p)
            if j < len(self.points) and self.points[j] == p:
                self.points.pop(j)
                del self.owner[p]

    def lookup(self, key: str) -> str:
        """Owner of key: first point clockwise (hash >= key hash), wrapping around."""
        if not self.points:
            raise LookupError("empty ring")
        i = bisect.bisect_left(self.points, stable_hash(key))
        return self.owner[self.points[i % len(self.points)]]

    def assignment(self, keys: list) -> dict:
        return {k: self.lookup(k) for k in keys}


def moved_fraction(a: dict, b: dict) -> float:
    """Fraction of keys (present in both) whose owner differs."""
    common = a.keys() & b.keys()
    return sum(a[k] != b[k] for k in common) / len(common)


def rendezvous(key: str, nodes: list) -> str:
    """Highest random weight: argmax over nodes of stable_hash(f"{node}|{key}")."""
    return max(nodes, key=lambda n: stable_hash(f"{n}|{key}"))


def max_over_mean(assignment: dict) -> float:
    """Load imbalance: max keys on one node / mean keys per node (over nodes that appear)."""
    c = Counter(assignment.values())
    return max(c.values()) / (len(assignment) / len(c))
