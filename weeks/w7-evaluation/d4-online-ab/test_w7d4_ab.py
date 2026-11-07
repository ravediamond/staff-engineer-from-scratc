import random

import pytest

from w7d4_ab import cuped, peeking_false_positive_rate, srm_pvalue, two_prop_z, variance_reduction


def test_srm():
    assert srm_pvalue(50_000, 50_000) == pytest.approx(1.0)
    assert srm_pvalue(50_600, 49_400) < 0.001
    assert srm_pvalue(5_030, 4_970) > 0.5
    assert srm_pvalue(20_000, 80_000, ratio=0.2) == pytest.approx(1.0)


def test_two_prop_z():
    z, p = two_prop_z(1000, 10_000, 1100, 10_000)
    assert z == pytest.approx(2.315, abs=0.01) and p == pytest.approx(0.0206, abs=0.001)
    z, _ = two_prop_z(1100, 10_000, 1000, 10_000)
    assert z < 0


def test_cuped():
    rng = random.Random(0)
    x = [rng.gauss(10, 3) for _ in range(5000)]
    y = [0.8 * xi + rng.gauss(0, 1.8) for xi in x]
    adj, theta = cuped(y, x)
    assert theta == pytest.approx(0.8, abs=0.03)
    assert sum(adj) / len(adj) == pytest.approx(sum(y) / len(y)), "CUPED keeps the mean"
    vr = variance_reduction(y, x)
    assert 0.6 < vr < 0.7  # rho^2 = 0.72 / (0.72 + 0.405 * ...) ~ 0.64


def test_peeking_inflates_and_bonferroni_fixes():
    naive = peeking_false_positive_rate(400, looks=10, n_per_look=200, seed=1)
    fixed = peeking_false_positive_rate(400, looks=10, n_per_look=200, seed=1, correct=True)
    assert naive > 0.12
    assert fixed < 0.06
