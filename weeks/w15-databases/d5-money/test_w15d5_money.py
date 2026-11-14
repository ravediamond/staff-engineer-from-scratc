import pytest

from w15d5_money import Ledger, LedgerError, SeatHolds, reconcile


def test_double_entry_and_derived_balances():
    led = Ledger()
    assert led.transfer("t1", "bank", "alice", 10_000) is True
    assert led.transfer("t2", "alice", "bob", 2_550) is True
    assert led.balance("alice") == 7_450 and led.balance("bob") == 2_550 and led.balance("bank") == -10_000
    assert led.balance("nobody") == 0 and led.trial_balance() == 0
    assert led.entries[-2:] == [("t2", "alice", -2_550), ("t2", "bob", 2_550)]


def test_idempotency():
    led = Ledger()
    led.transfer("fund", "bank", "alice", 5_000)
    assert led.transfer("pay-1", "alice", "bob", 1_000) is True
    assert led.transfer("pay-1", "alice", "bob", 1_000) is False, "a retry changes nothing"
    assert led.balance("bob") == 1_000 and len(led.entries) == 4
    with pytest.raises(LedgerError):
        led.transfer("pay-1", "alice", "bob", 9_999)
    assert led.balance("bob") == 1_000


def test_validation_and_overdraft_write_nothing():
    led = Ledger()
    led.no_overdraft.add("alice")
    led.transfer("fund", "bank", "alice", 1_000)
    for bad in (10.5, 10.0, -5, 0, True, "10"):
        with pytest.raises(LedgerError):
            led.transfer(f"bad-{bad}", "alice", "bob", bad)
    with pytest.raises(LedgerError):
        led.transfer("self", "alice", "alice", 100)
    with pytest.raises(LedgerError):
        led.transfer("too-much", "alice", "bob", 1_001)
    assert len(led.entries) == 2 and led.trial_balance() == 0
    assert led.transfer("too-much", "alice", "bob", 1_000) is True, "a failed attempt must not have reserved the key"
    assert led.balance("alice") == 0


def test_holds_expire_and_confirm_is_guarded():
    seats = SeatHolds(ttl=120)
    assert seats.hold("A1", "ana", now=0)
    assert not seats.hold("A1", "bo", now=119)
    assert seats.hold("A1", "ana", now=100), "the holder may renew"
    assert not seats.hold("A1", "bo", now=219)
    assert seats.hold("A1", "bo", now=220), "expired exactly at expires_at"
    assert not seats.confirm("A1", "ana", now=221), "ana's hold was taken over"
    assert not seats.confirm("A1", "bo", now=340), "bo waited too long"
    assert seats.hold("A1", "bo", now=341) and seats.confirm("A1", "bo", now=400)
    assert seats.confirm("A1", "bo", now=9999), "confirm is idempotent for the owner"
    assert not seats.hold("A1", "ana", now=10000) and not seats.confirm("A1", "ana", now=10000)
    assert not seats.confirm("B2", "ana", now=0), "no hold, no sale"


def test_reconcile():
    ours = {"p1": 1000, "p2": 2500, "p3": 990, "p5": 100}
    theirs = {"p1": 1000, "p2": 2400, "p3": 990, "p4": 700}
    assert reconcile(ours, theirs) == {"missing_from_ours": ["p4"], "missing_from_theirs": ["p5"],
                                       "amount_mismatch": ["p2"]}
