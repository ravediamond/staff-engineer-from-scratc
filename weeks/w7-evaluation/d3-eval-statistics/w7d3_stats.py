"""W7 D3: Wilson interval, exact McNemar, Holm correction, sample size and MDE for two proportions."""
import math
from statistics import NormalDist


def wilson(successes: int, n: int, z: float = 1.96) -> tuple:
    """(lo, hi) Wilson score interval."""
    if n == 0:
        return 0.0, 1.0
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, center - half), min(1.0, center + half)


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact p-value: 2 * P(X <= min(b, c)) with X ~ Binomial(b + c, 0.5), capped at 1.
    No discordant pairs -> 1.0."""
    m = b + c
    if m == 0:
        return 1.0
    k = min(b, c)
    return min(1.0, 2 * sum(math.comb(m, i) for i in range(k + 1)) / 2 ** m)


def holm(pvals: list, alpha: float = 0.05) -> list:
    """Booleans (same order as pvals): which hypotheses are rejected by Holm's step-down procedure."""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    rejected = [False] * m
    for rank, i in enumerate(order):
        if pvals[i] <= alpha / (m - rank):
            rejected[i] = True
        else:
            break
    return rejected


def n_per_arm(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Two-sided, unpaired, normal approximation (formula in README). Ceil."""
    za = NormalDist().inv_cdf(1 - alpha / 2)
    zb = NormalDist().inv_cdf(power)
    pbar = (p1 + p2) / 2
    num = (za * math.sqrt(2 * pbar * (1 - pbar)) + zb * math.sqrt(p1 * (1 - p1) + p2 * (1 - p2))) ** 2
    return math.ceil(num / (p1 - p2) ** 2)


def mde(n: int, p: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest d (to 0.001 resolution, d in (0, 1 - p)) such that n_per_arm(p, p + d) <= n."""
    d = 0.001
    while p + d < 1:
        if n_per_arm(p, p + d, alpha, power) <= n:
            return round(d, 3)
        d += 0.001
    return float("nan")
