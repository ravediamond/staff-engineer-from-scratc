"""W10 D5: exact speculative decoding acceptance, and its expected gain."""
import numpy as np


def speculative_step(p_dists: list, q_dists: list, drafted: list, rng: np.random.Generator) -> list:
    """p_dists: k+1 target distributions (one per drafted position, plus one for the bonus token).
    q_dists: k draft distributions. drafted: k token ids sampled from q_dists.
    For i in range(k): accept drafted[i] with prob min(1, p[i][x] / q[i][x]); if rejected, sample from
    normalize(max(0, p[i] - q[i])), append it, and return. If all accepted, append a sample from p_dists[k].
    Use rng.random() for the accept test and rng.choice(len(dist), p=dist) for sampling."""
    # TODO
    raise NotImplementedError


def expected_tokens(alpha: float, k: int) -> float:
    """(1 - alpha^(k+1)) / (1 - alpha); k + 1 if alpha == 1."""
    # TODO
    raise NotImplementedError


def speedup(alpha: float, k: int, c: float) -> float:
    # TODO
    raise NotImplementedError
