"""W2 D4: three rate limiters + a keyed wrapper. All time injected via clock()."""
from collections import deque


class TokenBucket:
    def __init__(self, rate: float, capacity: float, clock):
        self.rate, self.capacity, self.clock = rate, capacity, clock
        self.tokens = capacity
        self.last = clock()

    def _refill(self) -> None:
        now = self.clock()
        self.tokens = min(self.capacity, self.tokens + (now - self.last) * self.rate)
        self.last = now

    def allow(self, cost: float = 1) -> bool:
        self._refill()
        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


class SlidingWindowLog:
    """Exact: at most `limit` allowed events in any window (now - window, now]."""

    def __init__(self, limit: int, window: float, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self.log: deque = deque()

    def allow(self) -> bool:
        now = self.clock()
        while self.log and self.log[0] <= now - self.window:
            self.log.popleft()
        if len(self.log) < self.limit:
            self.log.append(now)
            return True
        return False


class SlidingWindowCounter:
    """Approximate: estimate = prev * (1 - elapsed_fraction) + curr, windows aligned to multiples of `window`."""

    def __init__(self, limit: int, window: float, clock):
        self.limit, self.window, self.clock = limit, window, clock
        self.win_start = (clock() // window) * window
        self.curr = 0
        self.prev = 0

    def allow(self) -> bool:
        now = self.clock()
        start = (now // self.window) * self.window
        if start != self.win_start:
            self.prev = self.curr if start - self.win_start == self.window else 0
            self.curr = 0
            self.win_start = start
        frac = (now - self.win_start) / self.window
        estimate = self.prev * (1 - frac) + self.curr
        if estimate + 1 <= self.limit:
            self.curr += 1
            return True
        return False


class KeyedLimiter:
    """One limiter per key, created lazily by factory()."""

    def __init__(self, factory):
        self.factory = factory
        self.limiters: dict = {}

    def allow(self, key, *args) -> bool:
        lim = self.limiters.get(key)
        if lim is None:
            lim = self.limiters[key] = self.factory()
        return lim.allow(*args)
