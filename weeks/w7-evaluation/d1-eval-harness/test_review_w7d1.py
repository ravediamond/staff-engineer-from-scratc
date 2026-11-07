import random

from review_w7d1 import delta_ci


def test_review_paired():
    rng = random.Random(1)
    base = [rng.random() for _ in range(150)]
    new = [b - 0.03 for b in base]
    lo, hi = delta_ci(base, new)
    assert hi < 0, "a consistent 3-point loss must be significant"
