from review_w11d2 import minimize


def test_review_shrinks():
    shrink = lambda x: [x // 2, x - 1] if x > 0 else []
    assert minimize(1000, lambda v: v >= 17, shrink) == 17
