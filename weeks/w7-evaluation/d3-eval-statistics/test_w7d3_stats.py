import math

import pytest

from w7d3_stats import holm, mcnemar_exact, mde, n_per_arm, wilson


def test_wilson():
    lo, hi = wilson(47, 50)
    assert lo == pytest.approx(0.8378, abs=1e-3) and hi == pytest.approx(0.9794, abs=1e-3)
    lo, hi = wilson(0, 20)
    assert lo == 0.0 and 0.15 < hi < 0.17
    assert wilson(10, 10)[1] == 1.0


def test_mcnemar():
    assert mcnemar_exact(0, 0) == 1.0
    assert mcnemar_exact(30, 30) == 1.0
    assert mcnemar_exact(40, 20) == pytest.approx(0.0135, abs=1e-3)
    assert mcnemar_exact(10, 0) == pytest.approx(2 / 1024)


def test_holm():
    assert holm([0.01, 0.04, 0.03, 0.005], 0.05) == [True, False, False, True]
    assert holm([0.001, 0.2], 0.05) == [True, False]
    assert holm([0.06], 0.05) == [False]


def test_sample_size_and_mde():
    assert n_per_arm(0.8, 0.85) == 906
    assert n_per_arm(0.5, 0.6) < n_per_arm(0.5, 0.55)
    d = mde(200, 0.8)
    assert 0.08 < d < 0.11
    assert n_per_arm(0.8, 0.8 + d) <= 200 < n_per_arm(0.8, 0.8 + d - 0.001)
