"""Review: an automated bisect bot. It blamed the wrong commit, off by one, on every incident.
Find the bug, fix it, explain:

WHY:
"""


def first_bad(n, is_bad):
    """0 is good, n-1 is bad."""
    lo, hi = 0, n - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if is_bad(mid):
            hi = mid
        else:
            lo = mid
    return lo
