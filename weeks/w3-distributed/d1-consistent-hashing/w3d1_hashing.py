"""W3 D1: consistent hashing ring with virtual nodes, and rendezvous hashing."""
import bisect
import hashlib
from collections import Counter


def stable_hash(s: str) -> int:
    """Deterministic across processes: first 8 bytes of MD5, big-endian."""
    # TODO
    raise NotImplementedError


class Ring:
    def __init__(self, vnodes: int = 100):
        self.vnodes = vnodes
        self.points: list = []   # sorted hashes
        self.owner: dict = {}    # hash -> node

    def add(self, node: str) -> None:
        """Insert `vnodes` points named f"{node}#{i}"."""
        # TODO
        raise NotImplementedError

    def remove(self, node: str) -> None:
        # TODO
        raise NotImplementedError

    def lookup(self, key: str) -> str:
        """Owner of key: first point clockwise (hash >= key hash), wrapping around."""
        # TODO
        raise NotImplementedError

    def assignment(self, keys: list) -> dict:
        # TODO
        raise NotImplementedError


def moved_fraction(a: dict, b: dict) -> float:
    """Fraction of keys (present in both) whose owner differs."""
    # TODO
    raise NotImplementedError


def rendezvous(key: str, nodes: list) -> str:
    """Highest random weight: argmax over nodes of stable_hash(f"{node}|{key}")."""
    # TODO
    raise NotImplementedError


def max_over_mean(assignment: dict) -> float:
    """Load imbalance: max keys on one node / mean keys per node (over nodes that appear)."""
    # TODO
    raise NotImplementedError
