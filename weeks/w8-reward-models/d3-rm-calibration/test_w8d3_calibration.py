import random

import pytest
import torch

from w8d3_calibration import ece, fit_temperature, length_bias, nll, pearson


def test_ece_weighting():
    probs = [0.95] * 100
    labels = [1] * 70 + [0] * 30
    assert ece(probs, labels) == pytest.approx(0.25)
    probs2 = [0.95] * 99 + [0.05]
    labels2 = [1] * 94 + [0] * 5 + [1]
    # big bin nearly calibrated, one-sample bin badly wrong: weighted ECE stays small
    assert ece(probs2, labels2) < 0.03
    assert ece([1.0, 0.0], [1, 0]) == 0.0


def test_temperature_scaling_fixes_overconfidence():
    g = torch.Generator().manual_seed(0)
    true_m = torch.randn(4000, generator=g) * 1.5
    labels = (torch.rand(4000, generator=g) < torch.sigmoid(true_m)).long()
    overconfident = true_m * 3
    T = fit_temperature(overconfident, labels)
    assert T == pytest.approx(3.0, rel=0.15)
    assert nll(overconfident, labels, T) < nll(overconfident, labels, 1.0)
    p_before = torch.sigmoid(overconfident).tolist()
    p_after = torch.sigmoid(overconfident / T).tolist()
    assert ece(p_after, labels.tolist()) < ece(p_before, labels.tolist())


def test_length_bias():
    rng = random.Random(0)
    lengths = [rng.randint(50, 500) for _ in range(500)]
    biased = [0.002 * l + rng.gauss(0, 0.3) for l in lengths]
    clean = [rng.gauss(0, 0.3) for _ in lengths]
    assert length_bias(biased, lengths) > 0.6
    assert abs(length_bias(clean, lengths)) < 0.1
    assert pearson([1, 2, 3], [2, 4, 6]) == pytest.approx(1.0)
