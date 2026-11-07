"""Review: CUPED implementation in the experimentation library. Variance 'reduction' is tiny, and on some
metrics it makes things worse. Find the bug, fix it, explain:

WHY:
"""
import statistics


def cuped_theta(y, x):
    mx, my = statistics.fmean(x), statistics.fmean(y)
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y)) / (len(x) - 1)
    return cov / statistics.variance(x)
