import random

import pytest

from w2d1_retry import (DeadlineExceeded, PermanentError, RetryableError, RetryBudget, backoff_delay,
                        call_with_retry, is_retryable_status)


class FakeTime:
    def __init__(self):
        self.t = 0.0
        self.sleeps = []
        self.sleep_ends = []

    def clock(self):
        return self.t

    def sleep(self, d):
        self.sleeps.append(d)
        self.t += d
        self.sleep_ends.append(self.t)


def test_status_classes():
    assert all(is_retryable_status(c) for c in [429, 500, 502, 503, 504])
    assert not any(is_retryable_status(c) for c in [200, 400, 401, 403, 404, 409, 422])


def test_full_jitter_bounds():
    rng = random.Random(0)
    for attempt in range(10):
        ds = [backoff_delay(attempt, 0.1, 5.0, rng) for _ in range(500)]
        hi = min(5.0, 0.1 * 2 ** attempt)
        assert all(0 <= d <= hi for d in ds)
        assert max(ds) > 0.8 * hi and min(ds) < 0.2 * hi, "full jitter spreads over [0, hi]"


def test_succeeds_after_transient_failures():
    ft, calls = FakeTime(), []

    def fn(remaining):
        calls.append(remaining)
        if len(calls) < 3:
            raise RetryableError("503")
        return "ok"

    out = call_with_retry(fn, max_attempts=5, base=0.1, cap=1, deadline=10, clock=ft.clock, sleep=ft.sleep,
                          rng=random.Random(1))
    assert out == "ok" and len(calls) == 3 and len(ft.sleeps) == 2
    assert calls[0] == 10 and calls[1] < 10, "fn receives the remaining budget"


def test_permanent_error_not_retried():
    ft, n = FakeTime(), [0]

    def fn(_):
        n[0] += 1
        raise PermanentError("400")

    with pytest.raises(PermanentError):
        call_with_retry(fn, max_attempts=5, base=0.1, cap=1, deadline=10, clock=ft.clock, sleep=ft.sleep,
                        rng=random.Random(0))
    assert n[0] == 1 and ft.sleeps == []


def test_out_of_attempts_raises_last():
    ft = FakeTime()

    def fn(_):
        raise RetryableError("again")

    with pytest.raises(RetryableError):
        call_with_retry(fn, max_attempts=3, base=0.01, cap=0.02, deadline=100, clock=ft.clock, sleep=ft.sleep,
                        rng=random.Random(0))
    assert len(ft.sleeps) == 2


def test_deadline_stops_retries():
    ft, n = FakeTime(), [0]

    def fn(_):
        n[0] += 1
        ft.t += 0.4  # each attempt takes 0.4 s
        raise RetryableError("slow")

    with pytest.raises(DeadlineExceeded):
        call_with_retry(fn, max_attempts=100, base=0.5, cap=0.5, deadline=1.0, clock=ft.clock, sleep=ft.sleep,
                        rng=random.Random(0))
    assert all(end < 1.0 for end in ft.sleep_ends), "never sleep past the deadline"
    assert n[0] <= 3


def test_retry_budget():
    t = [0.0]
    b = RetryBudget(ratio=0.1, min_per_window=2, window=10, clock=lambda: t[0])
    assert b.try_spend() and b.try_spend()
    assert not b.try_spend(), "only min_per_window retries with no traffic"
    for _ in range(100):
        b.record_request()
    spent = sum(b.try_spend() for _ in range(50))
    assert spent == 10, "2 + 10% of 100 = 12 total, 2 already spent"
    t[0] = 10.5
    assert b.try_spend() and b.try_spend() and not b.try_spend(), "window slid: back to the minimum"
