"""Review: comparison script used to approve prompt changes. It approved a change that consistently
lost 3 points on every case. Find the bug, fix it, explain:

WHY:
"""
import random


def delta_ci(base: list, new: list, n_boot=2000, seed=0):
    """base[i], new[i]: scores of the same case i under two systems."""
    rng = random.Random(seed)
    n = len(base)
    ds = []
    for _ in range(n_boot):
        a = [base[rng.randrange(n)] for _ in range(n)]
        b = [new[rng.randrange(n)] for _ in range(n)]
        ds.append(sum(b) / n - sum(a) / n)
    ds.sort()
    return ds[int(0.025 * n_boot)], ds[int(0.975 * n_boot) - 1]
