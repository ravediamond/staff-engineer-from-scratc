from review_w2d2 import Breaker


def test_review_half_open_admits_one():
    t = [0.0]
    b = Breaker(threshold=2, reset_timeout=5, clock=lambda: t[0])
    b.failure()
    b.failure()
    t[0] = 6
    admitted = sum(b.allow() for _ in range(100))
    assert admitted == 1
