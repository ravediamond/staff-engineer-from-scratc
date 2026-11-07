import numpy as np
import pytest

from w10d5_speculative import expected_tokens, speculative_step, speedup


def test_first_token_distribution_is_exactly_target():
    rng = np.random.default_rng(0)
    p = np.array([0.5, 0.3, 0.15, 0.05])
    q = np.array([0.1, 0.6, 0.1, 0.2])
    n = 20_000
    counts = np.zeros(4)
    for _ in range(n):
        x = int(rng.choice(4, p=q))
        out = speculative_step([p, p], [q], [x], rng)
        counts[out[0]] += 1
    emp = counts / n
    assert np.allclose(emp, p, atol=0.012), emp


def test_all_accepted_gets_bonus_token():
    rng = np.random.default_rng(1)
    p = [np.array([0.0, 1.0]), np.array([0.0, 1.0]), np.array([1.0, 0.0])]
    q = [np.array([0.0, 1.0]), np.array([0.0, 1.0])]
    assert speculative_step(p, q, [1, 1], rng) == [1, 1, 0]


def test_rejection_stops():
    rng = np.random.default_rng(2)
    p = [np.array([1.0, 0.0]), np.array([0.5, 0.5])]
    q = [np.array([0.0, 1.0])]
    assert speculative_step(p, q, [1], rng) == [0]


def test_formulas():
    assert expected_tokens(0.8, 4) == pytest.approx(3.3616)
    assert expected_tokens(1.0, 4) == 5
    assert expected_tokens(0.0, 4) == 1
    assert speedup(0.8, 4, 0.1) == pytest.approx(3.3616 / 1.4)
