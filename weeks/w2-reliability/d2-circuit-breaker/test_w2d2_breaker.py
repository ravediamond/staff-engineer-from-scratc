import pytest

from w2d2_breaker import CLOSED, HALF_OPEN, OPEN, CircuitBreaker, CircuitOpen


def make(t, **kw):
    args = dict(failure_threshold=3, reset_timeout=10, half_open_max=1, success_threshold=2, clock=lambda: t[0])
    args.update(kw)
    return CircuitBreaker(**args)


def boom():
    raise RuntimeError("down")


def test_trips_after_consecutive_failures():
    t = [0.0]
    b = make(t)
    for _ in range(2):
        with pytest.raises(RuntimeError):
            b.call(boom)
    b.call(lambda: "ok")  # success resets the count
    for _ in range(2):
        with pytest.raises(RuntimeError):
            b.call(boom)
    assert b.state == CLOSED
    with pytest.raises(RuntimeError):
        b.call(boom)
    assert b.state == OPEN
    with pytest.raises(CircuitOpen):
        b.call(lambda: "never called")


def test_half_open_after_timeout_and_limits_trials():
    t = [0.0]
    b = make(t, half_open_max=2)
    for _ in range(3):
        b.record_failure()
    t[0] = 9.99
    assert b.state == OPEN and not b.allow()
    t[0] = 10.0
    assert b.state == HALF_OPEN
    assert b.allow() and b.allow()
    assert not b.allow(), "only half_open_max trial calls in flight"


def test_half_open_success_closes():
    t = [0.0]
    b = make(t)
    for _ in range(3):
        b.record_failure()
    t[0] = 10
    assert b.allow()
    b.record_success()
    assert b.state == HALF_OPEN, "needs success_threshold=2 successes"
    assert b.allow()
    b.record_success()
    assert b.state == CLOSED


def test_half_open_failure_reopens_with_fresh_timer():
    t = [0.0]
    b = make(t)
    for _ in range(3):
        b.record_failure()
    t[0] = 10
    assert b.allow()
    b.record_failure()
    assert b.state == OPEN
    t[0] = 19.9
    assert b.state == OPEN, "timer restarted at t=10"
    t[0] = 20
    assert b.state == HALF_OPEN
