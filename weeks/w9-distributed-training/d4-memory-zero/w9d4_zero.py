"""W9 D4: model-state memory under DDP / ZeRO, and a ZeRO-1 step that matches full Adam."""
import numpy as np

GB = 1e9


def model_state_bytes(psi: float, mode: str, n: int = 1) -> float:
    """Per-GPU bytes for mixed-precision Adam model states. mode: 'ddp' | 'zero1' | 'zero2' | 'zero3'."""
    # TODO
    raise NotImplementedError


def max_params(gpu_gb: float, mode: str, n: int = 1, reserve_gb: float = 0.0) -> float:
    """Largest psi whose model states fit in (gpu_gb - reserve_gb). Model states are linear in psi."""
    # TODO
    raise NotImplementedError


def adam_step(p, g, m, v, t: int, lr: float = 1e-2, b1: float = 0.9, b2: float = 0.999, eps: float = 1e-8):
    """One Adam step (t starts at 1). Return new (p, m, v). Bias-corrected moments."""
    # TODO
    raise NotImplementedError


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
    # TODO
    raise NotImplementedError
