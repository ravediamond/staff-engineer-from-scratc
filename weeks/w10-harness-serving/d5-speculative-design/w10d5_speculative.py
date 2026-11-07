"""W10 D5: exact speculative decoding acceptance, and its expected gain."""
import numpy as np


def speculative_step(p_dists: list, q_dists: list, drafted: list, rng: np.random.Generator) -> list:
    """p_dists: k+1 target distributions (one per drafted position, plus one for the bonus token).
    q_dists: k draft distributions. drafted: k token ids sampled from q_dists.
    For i in range(k): accept drafted[i] with prob min(1, p[i][x] / q[i][x]); if rejected, sample from
    normalize(max(0, p[i] - q[i])), append it, and return. If all accepted, append a sample from p_dists[k].
    Use rng.random() for the accept test and rng.choice(len(dist), p=dist) for sampling."""
    out = []
    k = len(drafted)
    for i in range(k):
        x = drafted[i]
        p, q = np.asarray(p_dists[i]), np.asarray(q_dists[i])
        if rng.random() < min(1.0, p[x] / q[x]):
            out.append(x)
            continue
        resid = np.maximum(0.0, p - q)
        resid = resid / resid.sum()
        out.append(int(rng.choice(len(resid), p=resid)))
        return out
    last = np.asarray(p_dists[k])
    out.append(int(rng.choice(len(last), p=last)))
    return out


def expected_tokens(alpha: float, k: int) -> float:
    """(1 - alpha^(k+1)) / (1 - alpha); k + 1 if alpha == 1."""
    if alpha == 1:
        return k + 1
    return (1 - alpha ** (k + 1)) / (1 - alpha)


def speedup(alpha: float, k: int, c: float) -> float:
    return expected_tokens(alpha, k) / (1 + k * c)
