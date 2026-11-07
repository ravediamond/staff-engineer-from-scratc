"""W2 D4: three rate limiters + a keyed wrapper. All time injected via clock()."""
from collections import deque


class TokenBucket:
    def __init__(self, rate: float, capacity: float, clock):
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.tokens = capacity
        self.last = clock()

    def _refill(self) -> None:
        # TODO
        raise NotImplementedError

    def allow(self, cost: float = 1) -> bool:
        # TODO
        raise NotImplementedError


class SlidingWindowLog:
    """Exact: at most `limit` allowed events in any window (now - window, now]."""

    def __init__(self, limit: int, window: float, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self.log: deque = deque()

    def allow(self) -> bool:
        # TODO
        raise NotImplementedError


class SlidingWindowCounter:
    """Approximate: estimate = prev * (1 - elapsed_fraction) + curr, windows aligned to multiples of `window`."""

    def __init__(self, limit: int, window: float, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self.win_start = (clock() // window) * window
        self.curr = 0
        self.prev = 0

    def allow(self) -> bool:
        # TODO
        raise NotImplementedError


class KeyedLimiter:
    """One limiter per key, created lazily by factory()."""

    def __init__(self, factory):
        self.factory = factory
        self.limiters: dict = {}

    def allow(self, key, *args) -> bool:
        # TODO
        raise NotImplementedError
