import pytest

from review_w10d4 import kv_gb


def test_review_k_and_v():
    assert kv_gb(32, 8, 128, 1000, 1) == pytest.approx(0.131072)
