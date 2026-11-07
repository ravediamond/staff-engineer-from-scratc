"""W7 D4: online experiment statistics (no scipy)."""
import math
import random
import statistics


def _p_two_sided(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


def srm_pvalue(n_a: int, n_b: int, ratio: float = 0.5) -> float:
    """Chi-square goodness of fit (df=1) for the expected split ratio (share of A). p = erfc(sqrt(chi2/2))."""
    # TODO
    raise NotImplementedError


def two_prop_z(conv_a: int, n_a: int, conv_b: int, n_b: int) -> tuple:
    """Pooled two-proportion z-test. Return (z, two-sided p). z > 0 means B converts better."""
    # TODO
    raise NotImplementedError


def cuped(y: list, x: list) -> tuple:
    """theta = cov(x, y) / var(x) (sample cov/var, same ddof). y_adj_i = y_i - theta * (x_i - mean(x))."""
    # TODO
    raise NotImplementedError


def variance_reduction(y: list, x: list) -> float:
    """1 - var(y_adj) / var(y)."""
    # TODO
    raise NotImplementedError


def peeking_false_positive_rate(n_sims: int, looks: int, n_per_look: int, p: float = 0.1,
                                alpha: float = 0.05, seed: int = 0, correct: bool = False) -> float:
    """A/A test (both arms convert with probability p). After each look (n_per_look new users per arm),
    run two_prop_z on the cumulative data; stop and count a false positive at the first p-value < threshold.
    threshold = alpha / looks if correct else alpha. Use random.Random(seed). Return the FP rate."""
    # TODO
    raise NotImplementedError
