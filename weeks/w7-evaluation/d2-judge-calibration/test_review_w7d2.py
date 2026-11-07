import pytest

from review_w7d2 import kappa


def test_review_chance_uses_both_raters():
    human = ["pass"] * 80 + ["fail"] * 20
    judge = ["pass"] * 98 + ["fail"] * 2
    po = (80 + 2) / 100
    pe = 0.8 * 0.98 + 0.2 * 0.02
    assert kappa(human, judge) == pytest.approx((po - pe) / (1 - pe))
