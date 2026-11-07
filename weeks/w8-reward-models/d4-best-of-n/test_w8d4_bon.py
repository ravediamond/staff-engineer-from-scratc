import random

import pytest

from w8d4_bon import best_of_n, bon_kl, gold, gold_peak_n, overoptimization_curve, proxy, sample


def test_kl():
    assert bon_kl(1) == 0.0
    assert bon_kl(16) == pytest.approx(1.835, abs=1e-3)
    assert bon_kl(1024) > bon_kl(256) > bon_kl(64)


def test_scores_and_pick():
    assert proxy((1.0, 2.0)) == pytest.approx(4.0)
    assert gold((1.0, 2.0)) == pytest.approx(-0.2)
    s = [(0.0, 0.0), (0.5, 3.0), (1.0, 0.1)]
    assert best_of_n(s, proxy) == (0.5, 3.0)
    assert best_of_n(s, gold) == (1.0, 0.1)


def test_overoptimization_shape():
    ns = [1, 2, 4, 8, 16, 32, 64, 128, 256]
    curve = overoptimization_curve(ns, trials=400, seed=0)
    proxies = [row[2] for row in curve]
    golds = [row[3] for row in curve]
    assert all(b > a for a, b in zip(proxies, proxies[1:])), "proxy keeps rising"
    peak = gold_peak_n(curve)
    assert 4 <= peak <= 64
    assert golds[-1] < max(golds) - 0.1, "gold falls after the peak"
