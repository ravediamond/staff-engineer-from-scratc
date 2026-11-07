"""W7 D1: eval harness with repeats, flakiness, slices, paired bootstrap and a regression gate."""
import random
import statistics
from collections import defaultdict


def run_eval(cases: list, system, metric, repeats: int = 1) -> dict:
    """cases: [{"id", "input", "expected", "slice"}]. system(input, repeat_index) -> output.
    metric(output, expected) -> float. Return {id: (mean, population std)} over repeats."""
    out = {}
    for c in cases:
        scores = [metric(system(c["input"], r), c["expected"]) for r in range(repeats)]
        out[c["id"]] = (statistics.fmean(scores), statistics.pstdev(scores))
    return out


def flaky(results: dict, tol: float = 1e-9) -> list:
    """Sorted ids whose std > tol."""
    return sorted(cid for cid, (_, sd) in results.items() if sd > tol)


def slice_means(scores: dict, cases: list) -> dict:
    """scores: {id: float}. Return {slice: mean score} over cases present in scores."""
    acc = defaultdict(list)
    for c in cases:
        if c["id"] in scores:
            acc[c["slice"]].append(scores[c["id"]])
    return {s: statistics.fmean(v) for s, v in acc.items()}


def paired_bootstrap(base: dict, new: dict, n_boot: int = 2000, seed: int = 0) -> tuple:
    """Mean of (new - base) over common ids, and a 95% percentile CI from resampling ids with replacement
    (random.Random(seed)). Sort ids before resampling for determinism. lo/hi at int(0.025*n) and int(0.975*n)-1."""
    ids = sorted(base.keys() & new.keys())
    d = [new[i] - base[i] for i in ids]
    rng = random.Random(seed)
    n = len(d)
    means = sorted(sum(rng.choices(d, k=n)) / n for _ in range(n_boot))
    return sum(d) / n, means[int(0.025 * n_boot)], means[int(0.975 * n_boot) - 1]


def gate(base: dict, new: dict, cases: list, max_drop: float, slice_max_drop: float,
         n_boot: int = 2000, seed: int = 0) -> dict:
    """Fail reasons (in this order, include every one that applies):
       "significant regression"  if the paired CI upper bound < 0
       "mean drop"               if delta < -max_drop
       f"slice {name}"           for each slice (sorted by name) whose mean drops by more than slice_max_drop
    Return {"pass": not reasons, "reasons": reasons, "delta": (delta, lo, hi)}."""
    delta, lo, hi = paired_bootstrap(base, new, n_boot, seed)
    reasons = []
    if hi < 0:
        reasons.append("significant regression")
    if delta < -max_drop:
        reasons.append("mean drop")
    sb, sn = slice_means(base, cases), slice_means(new, cases)
    for name in sorted(sb):
        if name in sn and sn[name] - sb[name] < -slice_max_drop:
            reasons.append(f"slice {name}")
    return {"pass": not reasons, "reasons": reasons, "delta": (delta, lo, hi)}
