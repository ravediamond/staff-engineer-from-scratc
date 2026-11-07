import pytest

from w3d5_fencing import FencedStorage, LockService, StaleToken, simulate_gc_pause


def test_tokens_increase_and_expiry():
    t = [0.0]
    s = LockService(lease=10, clock=lambda: t[0])
    a = s.acquire("A")
    assert a == 1
    assert s.acquire("B") is None
    t[0] = 9.9
    assert s.acquire("B") is None
    t[0] = 10
    b = s.acquire("B")
    assert b == 2


def test_renew_and_release():
    t = [0.0]
    s = LockService(lease=10, clock=lambda: t[0])
    a = s.acquire("A")
    t[0] = 8
    assert s.renew("A", a)
    t[0] = 15
    assert s.acquire("B") is None, "renewed until 18"
    assert not s.renew("B", a)
    s.release("A", a)
    assert s.acquire("B") == 2


def test_renew_after_expiry_fails():
    t = [0.0]
    s = LockService(lease=10, clock=lambda: t[0])
    a = s.acquire("A")
    t[0] = 12
    assert not s.renew("A", a), "a client cannot resurrect an expired lease"


def test_storage_rejects_stale_tokens():
    st = FencedStorage()
    st.write("r", "v1", 5)
    st.write("r", "v1b", 5)
    with pytest.raises(StaleToken):
        st.write("r", "old", 4)
    st.write("other", "x", 1)
    assert st.data == {"r": "v1b", "other": "x"}


def test_gc_pause_scenario():
    final, accepted = simulate_gc_pause()
    assert final == "B" and accepted == ["B"]
