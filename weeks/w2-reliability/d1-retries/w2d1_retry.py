"""W2 D1: retries with full jitter, deadlines, and a retry budget. All time is injected."""
import random
from collections import deque


class RetryableError(Exception):
    """Transient failure: safe to retry."""


class PermanentError(Exception):
    """Will fail the same way again: never retry."""


class DeadlineExceeded(Exception):
    pass


RETRYABLE_STATUS = {429, 500, 502, 503, 504}


def is_retryable_status(code: int) -> bool:
    return code in RETRYABLE_STATUS


def backoff_delay(attempt: int, base: float, cap: float, rng: random.Random) -> float:
    """Full jitter: uniform(0, min(cap, base * 2**attempt)). attempt starts at 0."""
    return rng.uniform(0, min(cap, base * (2 ** attempt)))


def call_with_retry(fn, *, max_attempts: int, base: float, cap: float, deadline: float,
                    clock, sleep, rng: random.Random):
    """Call fn(remaining_seconds) until success.

    - RetryableError: back off and retry, if attempts remain and the sleep fits before `deadline`.
    - Any other exception: re-raise immediately.
    - Out of attempts: re-raise the last RetryableError.
    - Next sleep would end at or after the deadline: raise DeadlineExceeded (chained from the last error).
    - If the deadline has already passed before an attempt: raise DeadlineExceeded without calling fn.
    `deadline` is absolute, in the same units as clock().
    """
    last = None
    for attempt in range(max_attempts):
        remaining = deadline - clock()
        if remaining <= 0:
            raise DeadlineExceeded("no time left") from last
        try:
            return fn(remaining)
        except RetryableError as e:
            last = e
            if attempt == max_attempts - 1:
                raise
            d = backoff_delay(attempt, base, cap, rng)
            if clock() + d >= deadline:
                raise DeadlineExceeded("next retry would miss the deadline") from e
            sleep(d)
    raise AssertionError("unreachable")


class RetryBudget:
    """Allow retries only up to `ratio` of requests seen in the last `window` seconds,
    plus `min_per_window` retries always allowed (so low-traffic clients can still retry)."""

    def __init__(self, ratio: float, min_per_window: int, window: float, clock):
        self.ratio, self.min, self.window, self.clock = ratio, min_per_window, window, clock
        self.requests: deque = deque()
        self.retries: deque = deque()

    def _trim(self, q: deque) -> None:
        cutoff = self.clock() - self.window
        while q and q[0] <= cutoff:
            q.popleft()

    def record_request(self) -> None:
        self.requests.append(self.clock())

    def try_spend(self) -> bool:
        """True (and record the retry) if a retry is allowed now."""
        self._trim(self.requests)
        self._trim(self.retries)
        allowed = self.min + self.ratio * len(self.requests)
        if len(self.retries) + 1 <= allowed:
            self.retries.append(self.clock())
            return True
        return False
