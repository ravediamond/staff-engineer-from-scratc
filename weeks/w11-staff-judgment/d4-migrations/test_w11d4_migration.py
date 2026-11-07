import pytest

from w11d4_migration import Migration, MigrationError, backfill, verify


def test_backfill_resumable_and_versioned():
    old = {f"k{i:02d}": (1, i) for i in range(10)}
    new = {"k03": (2, "dual-written newer")}
    cp, rounds = None, 0
    while True:
        cp2 = backfill(old, new, batch=3, checkpoint=cp)
        if cp2 is None:
            break
        cp, rounds = cp2, rounds + 1
    assert rounds == 4
    assert new["k03"] == (2, "dual-written newer"), "never overwrite a newer version"
    assert all(new[k] == old[k] for k in old if k != "k03")
    assert backfill(old, new, 3, checkpoint="k09") is None


def test_verify():
    old = {"a": (1, "x"), "b": (2, "y"), "c": (1, "z"), "d": (1, "w")}
    new = {"a": (1, "x"), "b": (1, "y"), "c": (1, "DIFFERENT"), "d": (5, "newer")}
    rate, bad = verify(old, new)
    assert bad == ["b", "c"] and rate == 0.5
    assert verify({}, {}) == (0.0, [])


def test_state_machine_gates():
    m = Migration(threshold=0.001)
    assert m.advance() == "backfill"
    with pytest.raises(MigrationError):
        m.advance(backfill_done=False)
    assert m.advance(backfill_done=True) == "verify"
    with pytest.raises(MigrationError):
        m.advance(mismatch_rate=0.01)
    with pytest.raises(MigrationError):
        m.advance()
    assert m.read_from() == "old"
    assert m.advance(mismatch_rate=0.0005) == "cutover_reads" and m.read_from() == "new"
    with pytest.raises(MigrationError):
        m.advance(days_stable=3)
    assert m.rollback() == "dual_write" and m.read_from() == "old"


def test_no_rollback_after_stop_old_writes():
    m = Migration(0.01)
    m.advance()
    m.advance(backfill_done=True)
    m.advance(mismatch_rate=0.0)
    m.advance(days_stable=10)
    with pytest.raises(MigrationError):
        m.rollback()
    assert m.advance() == "cleanup"
