import random

from review_w7d4 import cuped_theta


def test_review_theta_regression_coefficient():
    rng = random.Random(0)
    x = [rng.gauss(0, 1) for _ in range(4000)]
    y = [2.0 * a + rng.gauss(0, 0.5) for a in x]
    assert abs(cuped_theta(y, x) - 2.0) < 0.1
