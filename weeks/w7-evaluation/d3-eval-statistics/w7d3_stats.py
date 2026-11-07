"""W7 D3: Wilson interval, exact McNemar, Holm correction, sample size and MDE for two proportions."""
import math
from statistics import NormalDist


def wilson(successes: int, n: int, z: float = 1.96) -> tuple:
    """(lo, hi) Wilson score interval."""
    # TODO
    raise NotImplementedError


def mcnemar_exact(b: int, c: int) -> float:
    """Two-sided exact p-value: 2 * P(X <= min(b, c)) with X ~ Binomial(b + c, 0.5), capped at 1.
    No discordant pairs -> 1.0."""
    # TODO
    raise NotImplementedError


def holm(pvals: list, alpha: float = 0.05) -> list:
    """Booleans (same order as pvals): which hypotheses are rejected by Holm's step-down procedure."""
    # TODO
    raise NotImplementedError


def n_per_arm(p1: float, p2: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """Two-sided, unpaired, normal approximation (formula in README). Ceil."""
    # TODO
    raise NotImplementedError


def mde(n: int, p: float, alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest d (to 0.001 resolution, d in (0, 1 - p)) such that n_per_arm(p, p + d) <= n."""
    # TODO
    raise NotImplementedError
