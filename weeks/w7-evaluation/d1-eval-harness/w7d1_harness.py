"""W7 D1: eval harness with repeats, flakiness, slices, paired bootstrap and a regression gate."""
import random
import statistics
from collections import defaultdict


def run_eval(cases: list, system, metric, repeats: int = 1) -> dict:
    """cases: [{"id", "input", "expected", "slice"}]. system(input, repeat_index) -> output.
    metric(output, expected) -> float. Return {id: (mean, population std)} over repeats."""
    # TODO
    raise NotImplementedError


def flaky(results: dict, tol: float = 1e-9) -> list:
    """Sorted ids whose std > tol."""
    # TODO
    raise NotImplementedError


def slice_means(scores: dict, cases: list) -> dict:
    """scores: {id: float}. Return {slice: mean score} over cases present in scores."""
    # TODO
    raise NotImplementedError


def paired_bootstrap(base: dict, new: dict, n_boot: int = 2000, seed: int = 0) -> tuple:
    """Mean of (new - base) over common ids, and a 95% percentile CI from resampling ids with replacement
    (random.Random(seed)). Sort ids before resampling for determinism. lo/hi at int(0.025*n) and int(0.975*n)-1."""
    # TODO
    raise NotImplementedError


def gate(base: dict, new: dict, cases: list, max_drop: float, slice_max_drop: float,
         n_boot: int = 2000, seed: int = 0) -> dict:
    """Fail reasons (in this order, include every one that applies):
       "significant regression"  if the paired CI upper bound < 0
       "mean drop"               if delta < -max_drop
       f"slice {name}"           for each slice (sorted by name) whose mean drops by more than slice_max_drop
    Return {"pass": not reasons, "reasons": reasons, "delta": (delta, lo, hi)}."""
    # TODO
    raise NotImplementedError
