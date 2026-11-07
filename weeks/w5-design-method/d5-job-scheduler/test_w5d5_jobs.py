from w5d5_jobs import JobQueue


def q(t, **kw):
    args = dict(lease_seconds=60, max_attempts=3, clock=lambda: t[0])
    args.update(kw)
    return JobQueue(**args)


def test_priority_then_fifo():
    t = [0.0]
    jq = q(t)
    for j in ["a", "b", "c"]:
        jq.submit(j, priority=5)
    jq.submit("urgent", priority=9)
    order = [jq.lease("w")[0] for _ in range(4)]
    assert order == ["urgent", "a", "b", "c"]
    assert jq.lease("w") is None


def test_delayed_job():
    t = [0.0]
    jq = q(t)
    jq.submit("later", priority=9, run_at=100)
    jq.submit("now", priority=1)
    assert jq.lease("w")[0] == "now"
    assert jq.lease("w") is None
    t[0] = 100
    assert jq.lease("w")[0] == "later"


def test_complete_and_stale_token():
    t = [0.0]
    jq = q(t)
    jq.submit("j", 1)
    jid, tok1 = jq.lease("slow")
    t[0] = 61
    jid2, tok2 = jq.lease("fast")
    assert jid2 == "j" and tok2 != tok1
    assert not jq.complete("j", tok1), "slow worker's lease expired"
    assert jq.complete("j", tok2)
    assert jq.state("j") == "done"
    assert not jq.complete("j", tok2), "double completion rejected"


def test_retries_then_dlq():
    t = [0.0]
    jq = q(t, max_attempts=2)
    jq.submit("poison", 1)
    _, tok = jq.lease("w")
    assert jq.fail("poison", tok)
    assert jq.state("poison") == "queued"
    _, tok = jq.lease("w")
    jq.fail("poison", tok)
    assert jq.state("poison") == "dead" and jq.dlq == ["poison"]
    assert jq.lease("w") is None


def test_expiry_counts_as_attempt():
    t = [0.0]
    jq = q(t, max_attempts=2)
    jq.submit("j", 1)
    jq.lease("w1")
    t[0] = 60
    jq.lease("w2")
    t[0] = 120
    jq.reap()
    assert jq.state("j") == "dead"
