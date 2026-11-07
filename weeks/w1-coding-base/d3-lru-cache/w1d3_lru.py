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
        n.prev.next, n.next.prev = n.next, n.prev

    def _push_front(self, n: _Node) -> None:
        n.prev, n.next = self.head, self.head.next
        self.head.next.prev = n
        self.head.next = n

    def _evict_lru(self) -> _Node:
        n = self.tail.prev
        self._unlink(n)
        del self.map[n.key]
        return n

    def get(self, key, default=None):
        n = self.map.get(key)
        if n is None:
            return default
        self._unlink(n)
        self._push_front(n)
        return n.val

    def put(self, key, value) -> None:
        n = self.map.get(key)
        if n is not None:
            n.val = value
            self._unlink(n)
            self._push_front(n)
            return
        n = _Node(key, value)
        self.map[key] = n
        self._push_front(n)
        if len(self.map) > self.cap:
            self._evict_lru()

    def __len__(self) -> int:
        return len(self.map)

    def keys_mru(self) -> list:
        """Keys from most to least recently used."""
        out, n = [], self.head.next
        while n is not self.tail:
            out.append(n.key)
            n = n.next
        return out


class TTLCache(LRUCache):
    """LRU + time-to-live. `clock()` returns seconds (injected for tests)."""

    def __init__(self, capacity: int, ttl: float, clock: Callable[[], float]):
        super().__init__(capacity)
        self.ttl = ttl
        self.clock = clock

    def put(self, key, value) -> None:
        super().put(key, value)
        self.map[key].expires = self.clock() + self.ttl

    def get(self, key, default=None):
        """Expired entries are removed on access and return default (lazy expiry)."""
        n = self.map.get(key)
        if n is None:
            return default
        if self.clock() >= n.expires:
            self._unlink(n)
            del self.map[key]
            return default
        return super().get(key, default)

    def purge_expired(self) -> int:
        """Remove every expired entry. Return how many were removed."""
        now, removed = self.clock(), 0
        for key, n in list(self.map.items()):
            if now >= n.expires:
                self._unlink(n)
                del self.map[key]
                removed += 1
        return removed
