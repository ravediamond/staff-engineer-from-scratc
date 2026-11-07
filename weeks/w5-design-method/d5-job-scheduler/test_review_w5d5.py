from review_w5d5 import Jobs


def test_review_stale_token_rejected():
    t = [0.0]
    jobs = Jobs(lambda: t[0])
    old = jobs.take("j")
    t[0] = 70
    new = jobs.take("j")
    assert not jobs.complete("j", old)
    assert jobs.complete("j", new)
