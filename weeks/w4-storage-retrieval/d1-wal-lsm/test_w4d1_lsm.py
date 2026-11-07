import json

import pytest

from w4d1_lsm import LSM, WAL


def test_wal_replay_and_torn_tail(tmp_path):
    w = WAL(tmp_path / "w.log")
    w.append({"k": "a", "v": 1})
    w.append({"k": "b", "v": 2})
    with open(tmp_path / "w.log", "a") as f:
        f.write('{"k": "c", "v')
    assert w.replay() == [{"k": "a", "v": 1}, {"k": "b", "v": 2}]


def test_wal_middle_corruption_raises(tmp_path):
    p = tmp_path / "w.log"
    p.write_text('{"k": "a", "v": 1}\nGARBAGE\n{"k": "b", "v": 2}\n')
    with pytest.raises(ValueError):
        WAL(p).replay()


def test_put_get_delete_overwrite(tmp_path):
    db = LSM(tmp_path, memtable_limit=3)
    for i in range(10):
        db.put(f"k{i}", i)
    db.put("k1", "new")
    db.delete("k2")
    assert db.get("k1") == "new"
    assert db.get("k2") is None
    assert db.get("k9") == 9
    assert db.get("missing", "dflt") == "dflt"
    assert len(db.sstables) >= 3


def test_newest_sstable_wins(tmp_path):
    db = LSM(tmp_path, memtable_limit=2)
    db.put("x", "v1")
    db.put("pad1", 0)  # flush 1
    db.put("x", "v2")
    db.put("pad2", 0)  # flush 2
    assert len(db.sstables) == 2 and not db.memtable
    assert db.get("x") == "v2"
    db.delete("x")
    db.put("pad3", 0)  # flush 3, tombstone in newest
    assert db.get("x") is None


def test_sstable_files_sorted(tmp_path):
    db = LSM(tmp_path, memtable_limit=3)
    for k in ["c", "a", "b"]:
        db.put(k, k)
    data = json.loads((tmp_path / "sst-0.json").read_text())
    assert [k for k, _ in data] == ["a", "b", "c"]


def test_recovery_from_wal_and_sstables(tmp_path):
    db = LSM(tmp_path, memtable_limit=3)
    for i in range(7):
        db.put(f"k{i}", i)
    db.delete("k0")
    del db  # "crash": memtable lost, WAL and SSTables on disk
    db2 = LSM(tmp_path, memtable_limit=3)
    assert [db2.get(f"k{i}") for i in range(7)] == [None, 1, 2, 3, 4, 5, 6]
