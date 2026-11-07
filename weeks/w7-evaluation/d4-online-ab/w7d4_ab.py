"""W7 D4: online experiment statistics (no scipy)."""
import math
import random
import statistics


def _p_two_sided(z: float) -> float:
    return math.erfc(abs(z) / math.sqrt(2))


def srm_pvalue(n_a: int, n_b: int, ratio: float = 0.5) -> float:
    """Chi-square goodness of fit (df=1) for the expected split ratio (share of A). p = erfc(sqrt(chi2/2))."""
    n = n_a + n_b
    ea, eb = n * ratio, n * (1 - ratio)
    chi2 = (n_a - ea) ** 2 / ea + (n_b - eb) ** 2 / eb
    return math.erfc(math.sqrt(chi2 / 2))


def two_prop_z(conv_a: int, n_a: int, conv_b: int, n_b: int) -> tuple:
    """Pooled two-proportion z-test. Return (z, two-sided p). z > 0 means B converts better."""
    pa, pb = conv_a / n_a, conv_b / n_b
    p = (conv_a + conv_b) / (n_a + n_b)
    se = math.sqrt(p * (1 - p) * (1 / n_a + 1 / n_b))
    z = (pb - pa) / se
    return z, _p_two_sided(z)


def cuped(y: list, x: list) -> tuple:
    """theta = cov(x, y) / var(x) (sample cov/var, same ddof). y_adj_i = y_i - theta * (x_i - mean(x))."""
    mx, my = statistics.fmean(x), statistics.fmean(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1)
    theta = cov / statistics.variance(x)
    return [b - theta * (a - mx) for a, b in zip(x, y)], theta


def variance_reduction(y: list, x: list) -> float:
    """1 - var(y_adj) / var(y)."""
    adj, _ = cuped(y, x)
    return 1 - statistics.variance(adj) / statistics.variance(y)


def peeking_false_positive_rate(n_sims: int, looks: int, n_per_look: int, p: float = 0.1,
                                alpha: float = 0.05, seed: int = 0, correct: bool = False) -> float:
    """A/A test (both arms convert with probability p). After each look (n_per_look new users per arm),
    run two_prop_z on the cumulative data; stop and count a false positive at the first p-value < threshold.
    threshold = alpha / looks if correct else alpha. Use random.Random(seed). Return the FP rate."""
    rng = random.Random(seed)
    thr = alpha / looks if correct else alpha
    fp = 0
    for _ in range(n_sims):
        ca = cb = n = 0
        for _ in range(looks):
            ca += sum(rng.random() < p for _ in range(n_per_look))
            cb += sum(rng.random() < p for _ in range(n_per_look))
            n += n_per_look
            if 0 < ca + cb < 2 * n and two_prop_z(ca, n, cb, n)[1] < thr:
                fp += 1
                break
    return fp / n_sims
