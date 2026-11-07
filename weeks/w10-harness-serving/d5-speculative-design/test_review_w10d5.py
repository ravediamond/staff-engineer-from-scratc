from review_w10d5 import accept_prob


def test_review_ratio_direction():
    assert accept_prob(0.6, 0.3) == 1.0
    assert abs(accept_prob(0.1, 0.4) - 0.25) < 1e-12
