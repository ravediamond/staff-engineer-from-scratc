"""W1 D3: LRU with a hand-written doubly linked list, and a TTL cache with an injected clock."""
from typing import Callable


class _Node:
    __slots__ = ("key", "val", "prev", "next", "expires")

    def __init__(self, key=None, val=None):
        self.key, self.val = key, val
        self.prev = self.next = None
        self.expires = float("inf")


class LRUCache:
    def __init__(self, capacity: int):
        assert capacity > 0
        self.cap = capacity
        self.map: dict = {}
        self.head, self.tail = _Node(), _Node()  # sentinels: head.next is MRU, tail.prev is LRU
        self.head.next, self.tail.prev = self.tail, self.head

    def _unlink(self, n: _Node) -> None:
        # TODO
        raise NotImplementedError

    def _push_front(self, n: _Node) -> None:
        # TODO
        raise NotImplementedError

    def _evict_lru(self) -> _Node:
        # TODO
        raise NotImplementedError

    def get(self, key, default=None):
        # TODO
        raise NotImplementedError

    def put(self, key, value) -> None:
        # TODO
        raise NotImplementedError

    def __len__(self) -> int:
        return len(self.map)

    def keys_mru(self) -> list:
        """Keys from most to least recently used."""
        # TODO
        raise NotImplementedError


class TTLCache(LRUCache):
    """LRU + time-to-live. `clock()` returns seconds (injected for tests)."""

    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float]):
        super().__init__(capacity)
        self.ttl = ttl
        self.clock = clock

    def put(self, key, value) -> None:
        # TODO
        raise NotImplementedError

    def get(self, key, default=None):
        """Expired entries are removed on access and return default (lazy expiry)."""
        # TODO
        raise NotImplementedError

    def purge_expired(self) -> int:
        """Remove every expired entry. Return how many were removed."""
        # TODO
        raise NotImplementedError
