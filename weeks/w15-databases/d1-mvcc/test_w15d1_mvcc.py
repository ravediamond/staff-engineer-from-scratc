import pytest

from w15d1_mvcc import MVCCStore, SerializationFailure, WriteConflict


def seeded(**values):
    db = MVCCStore()
    t = db.begin()
    for k, v in values.items():
        db.write(t, k, v)
    db.commit(t)
    return db


def test_snapshot_is_stable_read_committed_is_not():
    db = seeded(x=10)
    snap, rc = db.begin("snapshot"), db.begin("read_committed")
    assert db.read(snap, "x") == 10 and db.read(rc, "x") == 10
    w = db.begin()
    db.write(w, "x", 20)
    assert db.read(snap, "x") == 10 and db.read(rc, "x") == 10, "no dirty reads at any level"
    assert db.read(w, "x") == 20, "a transaction sees its own writes"
    db.commit(w)
    assert db.read(snap, "x") == 10, "repeatable read"
    assert db.read(rc, "x") == 20, "read committed sees every new commit"
    assert db.read(db.begin(), "x") == 20 and db.read(db.begin(), "missing") is None


def test_transaction_started_before_a_commit_does_not_see_it():
    db = seeded(x=1)
    w = db.begin()                 # in progress when `snap` begins
    snap = db.begin("snapshot")
    db.write(w, "x", 2)
    db.commit(w)
    assert db.read(snap, "x") == 1, "w was still active at snap's start: invisible even after it commits"


def test_aborted_writes_are_never_visible():
    db = seeded(x=1)
    t = db.begin()
    db.write(t, "x", 99)
    db.abort(t)
    assert db.read(db.begin(), "x") == 1
    t2 = db.begin()
    db.write(t2, "x", 2)           # an aborted version does not block or conflict
    db.commit(t2)
    assert db.read(db.begin("read_committed"), "x") == 2


def test_concurrent_uncommitted_writers_conflict():
    db = seeded(x=1)
    a, b = db.begin(), db.begin()
    db.write(a, "x", 2)
    with pytest.raises(WriteConflict):
        db.write(b, "x", 3)
    db.write(a, "x", 4)            # rewriting your own version is fine
    db.commit(a)
    assert db.read(db.begin(), "x") == 4 and len(db.versions["x"]) == 2


def test_lost_update_prevented_by_snapshot_isolation_not_by_read_committed():
    db = seeded(n=10)
    a, b = db.begin("snapshot"), db.begin("snapshot")
    va, vb = db.read(a, "n"), db.read(b, "n")
    db.write(a, "n", va + 1)
    db.commit(a)
    with pytest.raises(SerializationFailure):
        db.write(b, "n", vb + 1)

    db = seeded(n=10)
    a, b = db.begin("read_committed"), db.begin("read_committed")
    va, vb = db.read(a, "n"), db.read(b, "n")
    db.write(a, "n", va + 1)
    db.commit(a)
    db.write(b, "n", vb + 1)       # allowed: the application computed 11 from a stale read
    db.commit(b)
    assert db.read(db.begin(), "n") == 11, "one increment lost"


def on_call_shift(db, level):
    """Each doctor's transaction: if the other is on call, go off call."""
    alice, bob = db.begin(level), db.begin(level)
    if db.read(alice, "bob"):
        db.write(alice, "alice", False)
    if db.read(bob, "alice"):
        db.write(bob, "bob", False)
    db.commit(alice)
    db.commit(bob)


def test_write_skew_allowed_by_snapshot_caught_by_serializable():
    db = seeded(alice=True, bob=True)
    on_call_shift(db, "snapshot")
    final = db.begin()
    assert db.read(final, "alice") is False and db.read(final, "bob") is False, "nobody on call: write skew"

    db = seeded(alice=True, bob=True)
    with pytest.raises(SerializationFailure):
        on_call_shift(db, "serializable")
    final = db.begin()
    assert db.read(final, "alice") is False and db.read(final, "bob") is True
    assert not db.active - {final.id}, "the failed transaction was aborted"


def test_vacuum_respects_open_snapshots():
    db = seeded(x=0)
    old = db.begin("snapshot")
    for i in range(1, 4):
        t = db.begin()
        db.write(t, "x", i)
        db.commit(t)
    doomed = db.begin()
    db.write(doomed, "y", 1)
    db.abort(doomed)
    assert db.vacuum([old]) == 1, "only the aborted version: `old` still needs x=0 and the chain after it"
    assert db.read(old, "x") == 0
    db.commit(old)
    assert db.vacuum([]) == 3
    assert db.versions["x"] == [[5, 3]]
