import pytest

from w2d3_idempotency import IdempotencyStore, InFlight, KeyConflict, Ledger, fingerprint


def test_fingerprint_canonical():
    assert fingerprint({"b": 1, "a": [1, 2]}) == fingerprint({"a": [1, 2], "b": 1})
    assert fingerprint({"a": 1}) != fingerprint({"a": 2})
    assert len(fingerprint({})) == 64


def test_executes_once_and_replays_result():
    s = IdempotencyStore(ttl=100, clock=lambda: 0)
    calls = []
    r1 = s.execute("k", {"x": 1}, lambda: calls.append(1) or "done")
    r2 = s.execute("k", {"x": 1}, lambda: calls.append(1) or "again")
    assert r1 == r2 == "done" and len(calls) == 1


def test_conflict_on_different_payload():
    s = IdempotencyStore(ttl=100, clock=lambda: 0)
    s.execute("k", {"amount": 10}, lambda: "ok")
    with pytest.raises(KeyConflict):
        s.execute("k", {"amount": 99}, lambda: "other")


def test_in_flight():
    s = IdempotencyStore(ttl=100, clock=lambda: 0)

    def reentrant():
        with pytest.raises(InFlight):
            s.execute("k", {"a": 1}, lambda: "inner")
        return "outer"

    assert s.execute("k", {"a": 1}, reentrant) == "outer"


def test_failure_releases_key():
    s = IdempotencyStore(ttl=100, clock=lambda: 0)
    with pytest.raises(RuntimeError):
        s.execute("k", {"a": 1}, lambda: (_ for _ in ()).throw(RuntimeError("boom")))
    assert s.execute("k", {"a": 1}, lambda: "second try works") == "second try works"


def test_ttl_expiry():
    t = [0.0]
    s = IdempotencyStore(ttl=10, clock=lambda: t[0])
    s.execute("k", {"a": 1}, lambda: "first")
    t[0] = 10
    assert s.execute("k", {"a": 1}, lambda: "fresh") == "fresh"
    assert s.executions == 2


def test_ledger_exactly_once():
    s = IdempotencyStore(ttl=1000, clock=lambda: 0)
    led = Ledger({"alice": 100, "bob": 0}, s)
    for _ in range(5):  # client retries 5 times
        out = led.transfer("pay-1", "alice", "bob", 30)
    assert out == {"src": 70, "dst": 30}
    assert led.balances == {"alice": 70, "bob": 30}
    led.transfer("pay-2", "alice", "bob", 30)
    assert led.balances == {"alice": 40, "bob": 60}


def test_ledger_failed_transfer_retryable():
    s = IdempotencyStore(ttl=1000, clock=lambda: 0)
    led = Ledger({"alice": 10, "bob": 0}, s)
    with pytest.raises(ValueError):
        led.transfer("pay-1", "alice", "bob", 50)
    led.balances["alice"] = 100  # funds arrive
    assert led.transfer("pay-1", "alice", "bob", 50) == {"src": 50, "dst": 50}
