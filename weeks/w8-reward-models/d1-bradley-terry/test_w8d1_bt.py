import random

import pytest
import torch

from w8d1_bt import bt_fit, bt_log_likelihood, bt_prob, elo_expected, elo_update


def simulate(true_r, n, seed=0):
    rng = random.Random(seed)
    k = len(true_r)
    out = []
    for _ in range(n):
        i, j = rng.sample(range(k), 2)
        p = 1 / (1 + pow(2.718281828, -(true_r[i] - true_r[j])))
        out.append((i, j) if rng.random() < p else (j, i))
    return out


def test_prob_and_loglik():
    r = torch.tensor([1.0, 0.0])
    assert bt_prob(r, 0, 1).item() == pytest.approx(0.7311, abs=1e-4)
    assert bt_prob(r, 1, 0).item() == pytest.approx(1 - 0.7311, abs=1e-4)
    ll = bt_log_likelihood(r, [(0, 1), (1, 0)])
    assert ll.item() == pytest.approx(torch.log(torch.tensor(0.7311 * 0.2689)).item(), abs=1e-3)


def test_fit_recovers_ranking():
    true_r = [2.0, 1.0, 0.0, -0.5, -2.0]
    r = bt_fit(5, simulate(true_r, 3000))
    assert torch.argsort(r, descending=True).tolist() == [0, 1, 2, 3, 4]
    assert abs(r.mean().item()) < 1e-6
    assert (r[0] - r[4]).item() == pytest.approx(4.0, abs=0.6)


def test_l2_keeps_undefeated_finite():
    r = bt_fit(2, [(0, 1)] * 50, steps=300)
    assert torch.isfinite(r).all() and r[0] > r[1]


def test_elo():
    assert elo_expected(1600, 1400) == pytest.approx(0.7597, abs=1e-4)
    a, b = elo_update(1500, 1500, 1.0, k=32)
    assert (a, b) == (pytest.approx(1516), pytest.approx(1484))
    a, b = elo_update(1700, 1500, 0.5)
    assert a < 1700 and a + b == pytest.approx(3200)
