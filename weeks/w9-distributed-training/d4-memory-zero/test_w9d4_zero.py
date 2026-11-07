import numpy as np
import pytest

from w9d4_zero import adam_step, max_params, model_state_bytes, shard_slices, zero1_step


def test_memory_table():
    psi = 7e9
    assert model_state_bytes(psi, "ddp") == pytest.approx(112e9)
    assert model_state_bytes(psi, "zero1", 8) == pytest.approx(4 * psi + 12 * psi / 8)
    assert model_state_bytes(psi, "zero2", 8) == pytest.approx(2 * psi + 14 * psi / 8)
    assert model_state_bytes(psi, "zero3", 64) == pytest.approx(1.75e9)
    assert model_state_bytes(psi, "zero3", 1) == model_state_bytes(psi, "ddp")


def test_max_params():
    assert max_params(80, "ddp", reserve_gb=20) == pytest.approx(3.75e9)
    assert max_params(80, "zero3", 64, reserve_gb=20) == pytest.approx(240e9)


def test_adam_first_step_is_lr_times_sign():
    p = np.array([1.0, -1.0, 0.5])
    g = np.array([0.3, -2.0, 1e-3])
    p2, m, v = adam_step(p, g, np.zeros(3), np.zeros(3), t=1, lr=0.01)
    assert np.allclose(p2, p - 0.01 * np.sign(g), atol=1e-5)


def test_zero1_equals_full_adam():
    rng = np.random.default_rng(0)
    n_params, n = 23, 4
    p_full = rng.normal(size=n_params)
    m_full, v_full = np.zeros(n_params), np.zeros(n_params)
    p_z = p_full.copy()
    shards = shard_slices(n_params, n)
    states = [(np.zeros(sl.stop - sl.start), np.zeros(sl.stop - sl.start)) for sl in shards]
    for t in range(1, 11):
        grads = [rng.normal(size=n_params) for _ in range(n)]
        p_full, m_full, v_full = adam_step(p_full, sum(grads) / n, m_full, v_full, t)
        p_z, states = zero1_step(p_z, grads, states, t)
    assert np.allclose(p_full, p_z)
    assert np.allclose(np.concatenate([m for m, _ in states]), m_full)
