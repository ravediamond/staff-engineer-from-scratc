from review_w14d1 import Controller


def test_review_replayed_events_do_not_create_extra_workers():
    c = Controller(6)
    c.start()
    for name in ("worker-1", "worker-2", "worker-3"):
        c.on_event(("DELETED", name))
    assert len(c.workers) == 6
    for name in ("worker-1", "worker-2", "worker-3"):      # the watch reconnects and replays
        c.on_event(("DELETED", name))
    assert len(c.workers) == 6, f"{len(c.workers)} workers for replicas=6"
