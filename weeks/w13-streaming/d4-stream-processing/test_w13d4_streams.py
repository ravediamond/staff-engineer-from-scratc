from w13d4_streams import WindowedCounter


def feed(job, partition, events, start_offset=0):
    for i, (key, ts) in enumerate(events):
        job.process(partition, start_offset + i, key, ts)


def test_out_of_order_events_inside_the_bound_are_counted():
    job = WindowedCounter(1, window=60, max_out_of_order=10)
    feed(job, 0, [("a", 5), ("a", 50), ("a", 62), ("a", 58)])
    assert job.watermark() == 52 and job.emit() == []
    job.process(0, 4, "a", 71)
    assert job.watermark() == 61
    assert job.emit() == [(0, "a", 3)]
    assert job.emit() == [], "a result is emitted once unless it changes"


def test_watermark_is_min_over_partitions():
    job = WindowedCounter(2, window=60, max_out_of_order=10)
    feed(job, 0, [("a", 30), ("a", 500)])
    assert job.watermark() is None and job.emit() == [], "partition 1 has not spoken yet"
    job.process(1, 0, "b", 90)
    assert job.watermark() == 80
    assert job.emit() == [(0, "a", 1)]
    job.process(1, 1, "b", 45)        # late for partition 1's own order, but the window state is... gone?
    assert job.late == [(1, 1, "b", 45)], "window [0,60) closed at watermark 80 with no allowed lateness"


def test_allowed_lateness_updates_then_side_output():
    job = WindowedCounter(1, window=60, max_out_of_order=10, allowed_lateness=30)
    feed(job, 0, [("a", 10), ("a", 85)])
    assert job.emit() == [(0, "a", 1)]
    job.process(0, 2, "a", 20)                       # watermark 75 < 90: accepted, result updated
    assert job.emit() == [(0, "a", 2)]
    job.process(0, 3, "a", 105)                      # watermark -> 95 >= 90: window [0,60) is purged on emit
    job.emit()
    assert (0, "a") not in job.counts and (0, "a") not in job.emitted
    job.process(0, 4, "a", 30)
    assert job.late == [(0, 4, "a", 30)]
    assert all(start != 0 for start, _, _ in job.emit())


def test_lateness_uses_watermark_before_the_event():
    job = WindowedCounter(1, window=60, max_out_of_order=0)
    job.process(0, 0, "a", 10)
    job.process(0, 1, "a", 59)
    assert job.late == [] and job.counts[(0, "a")] == 2


def test_checkpoint_restore_replay_is_exactly_once():
    events = [("a", 5), ("b", 20), ("a", 70), ("a", 40), ("b", 130), ("a", 135), ("a", 200)]
    ref = WindowedCounter(1, 60, 10)
    ref_out = []
    for i, (k, ts) in enumerate(events):
        ref.process(0, i, k, ts)
        ref_out += ref.emit()

    job = WindowedCounter(1, 60, 10)
    out = []
    for i in range(3):
        job.process(0, i, *events[i])
        out += job.emit()
    snap = job.snapshot()
    for i in range(3, 6):                      # work done after the checkpoint, lost in the crash
        job.process(0, i, *events[i])
    job.restore(snap)
    job.counts[(999, "x")] = 1
    assert (999, "x") not in snap["counts"], "the snapshot must be a deep copy"
    del job.counts[(999, "x")]
    for i in range(1, len(events)):            # source rewinds too far: offsets 1-2 are duplicates
        accepted = job.process(0, i, *events[i])
        assert accepted == (i >= 3)
        out += job.emit()
    assert out == ref_out
