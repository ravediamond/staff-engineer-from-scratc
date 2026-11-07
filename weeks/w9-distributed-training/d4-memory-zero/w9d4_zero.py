"""W9 D4: model-state memory under DDP / ZeRO, and a ZeRO-1 step that matches full Adam."""
import numpy as np

GB = 1e9


def model_state_bytes(psi: float, mode: str, n: int = 1) -> float:
    """Per-GPU bytes for mixed-precision Adam model states. mode: 'ddp' | 'zero1' | 'zero2' | 'zero3'."""
    if mode == "ddp":
        return 16 * psi
    if mode == "zero1":
        return 4 * psi + 12 * psi / n
    if mode == "zero2":
        return 2 * psi + 14 * psi / n
    if mode == "zero3":
        return 16 * psi / n
    raise ValueError(mode)


def max_params(gpu_gb: float, mode: str, n: int = 1, reserve_gb: float = 0.0) -> float:
    """Largest psi whose model states fit in (gpu_gb - reserve_gb). Model states are linear in psi."""
    per_param = model_state_bytes(1.0, mode, n)
    return (gpu_gb - reserve_gb) * GB / per_param


def adam_step(p, g, m, v, t: int, lr: float = 1e-2, b1: float = 0.9, b2: float = 0.999, eps: float = 1e-8):
    """One Adam step (t starts at 1). Return new (p, m, v). Bias-corrected moments."""
    m = b1 * m + (1 - b1) * g
    v = b2 * v + (1 - b2) * g * g
    mhat = m / (1 - b1 ** t)
    vhat = v / (1 - b2 ** t)
    return p - lr * mhat / (np.sqrt(vhat) + eps), m, v


def shard_slices(n_params: int, n: int) -> list:
    """Provided: contiguous shard boundaries, like W9 D1's chunks."""
    base, extra = divmod(n_params, n)
    out, s = [], 0
    for i in range(n):
        e = s + base + (1 if i < extra else 0)
        out.append(slice(s, e))
        s = e
    return out


def zero1_step(params: np.ndarray, grads_per_rank: list, states: list, t: int, lr: float = 1e-2) -> tuple:
    """ZeRO-1. params: the full parameter vector (identical on every rank before the step).
    grads_per_rank: each rank's local gradient (full length). states[r] = (m_shard, v_shard) owned by rank r.
    1. average gradients (an all-reduce),
    2. each rank r updates params[shard_r] with adam_step using only its own (m, v) shard,
    3. all-gather: assemble the new full parameter vector from the updated shards.
    Return (new_params, new_states)."""
    n = len(grads_per_rank)
    g = sum(grads_per_rank) / n
    new = params.copy()
    new_states = []
    for r, sl in enumerate(shard_slices(len(params), n)):
        m, v = states[r]
        p_r, m, v = adam_step(params[sl], g[sl], m, v, t, lr)
        new[sl] = p_r
        new_states.append((m, v))
    return new, new_states
