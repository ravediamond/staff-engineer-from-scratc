import pytest

from w13d1_log import OffsetOutOfRange, PartitionLog


def filled(n, **kw):
    log = PartitionLog(**kw)
    for i in range(n):
        log.append(f"k{i}", f"v{i}", ts=1000 * i)
    return log


def test_append_rolls_segments_and_indexes():
    log = filled(10, segment_records=4, index_every=2)
    assert [s.base_offset for s in log.segments] == [0, 4, 8]
    assert [len(s.records) for s in log.segments] == [4, 4, 2]
    assert log.segments[1].index == [(4, 0), (6, 2)]
    assert log.next_offset == 10 and log.log_start_offset == 0
    assert log.append("x", "y", 0) == 10


def test_read_uses_the_index():
    log = filled(1000, segment_records=100, index_every=10)
    recs = log.read(557, max_records=3)
    assert [r.offset for r in recs] == [557, 558, 559]
    assert log.scans <= 10 + 3, f"scanned {log.scans} records: use the segment list and the sparse index"
    assert [r.offset for r in log.read(98, 5)] == [98, 99, 100, 101, 102], "reads continue into the next segment"
    assert log.read(1000) == []
    with pytest.raises(OffsetOutOfRange):
        log.read(1001)


def test_retention_keeps_active_and_unexpired():
    log = filled(10, segment_records=4)          # ts 0..9000
    assert log.apply_retention(now=20_000, retention_ms=14_000) == 1   # cutoff 6000: segment [0-3] newest ts 3000
    assert log.log_start_offset == 4
    with pytest.raises(OffsetOutOfRange):
        log.read(2)
    assert log.apply_retention(now=10**9, retention_ms=1) == 1          # everything expired
    assert len(log.segments) == 1 and log.segments[0].base_offset == 8, "the active segment is never deleted"
    assert [r.offset for r in log.read(8)] == [8, 9]


def test_retention_stops_at_first_live_segment():
    log = PartitionLog(segment_records=2)
    for ts in (0, 0, 9_000, 9_000, 0, 0, 5, 5):   # segment 2 is old but sits behind a live one
        log.append("k", "v", ts)
    assert log.apply_retention(now=10_000, retention_ms=5_000) == 1
    assert log.log_start_offset == 2


def test_compaction_keeps_latest_per_key_and_offsets():
    log = PartitionLog(segment_records=3, index_every=2)
    for key, value in [("k1", "a"), ("k2", "b"), ("k1", "c"), ("k2", None), ("k3", "d"), ("k4", "e"), ("k4", "f")]:
        log.append(key, value, 0)
    # segments: [0,1,2] [3,4,5] active [6]
    log.compact()
    assert [(r.offset, r.key, r.value) for r in log.read(0, 100)] == [(2, "k1", "c"), (4, "k3", "d"), (6, "k4", "f")]
    assert log.log_start_offset == 0 and log.next_offset == 7, "compaction does not move the log start"
    assert [r.offset for r in log.read(3)] == [4, 6], "a committed offset that fell into a gap resumes at the next record"
    assert log.append("k9", "z", 0) == 7


def test_compaction_leaves_active_segment_and_rebuilds_index():
    log = PartitionLog(segment_records=4, index_every=2)
    for i in range(8):
        log.append("same", i, 0)
    for i in range(2):
        log.append("other", i, 0)
    log.compact()
    assert [r.offset for r in log.segments[-1].records] == [8, 9], "active segment untouched (even its duplicates)"
    assert [r.offset for r in log.read(0, 100)] == [7, 8, 9]
    closed = log.segments[0]
    assert closed.index == [(7, 0)]
