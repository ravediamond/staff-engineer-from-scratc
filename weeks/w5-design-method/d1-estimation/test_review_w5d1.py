import pytest

from review_w5d1 import egress_gbps


def test_review_bits_not_bytes():
    assert egress_gbps(10_000, 125) == pytest.approx(10.0)
