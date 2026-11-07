import pytest

from review_w8d3 import ece


def test_review_weighted_by_bin_size():
    probs = [0.85] * 999 + [0.05]
    labels = [1] * 850 + [0] * 149 + [1]
    assert ece(probs, labels) == pytest.approx((999 * abs(850 / 999 - 0.85) + 1 * 0.95) / 1000)
