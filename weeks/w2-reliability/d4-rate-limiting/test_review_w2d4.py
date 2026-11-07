from review_w2d4 import Bucket


def test_review_idle_burst_capped():
    t = [0.0]
    b = Bucket(rate=5, capacity=10, clock=lambda: t[0])
    t[0] = 1000
    assert sum(b.allow() for _ in range(1000)) == 10
