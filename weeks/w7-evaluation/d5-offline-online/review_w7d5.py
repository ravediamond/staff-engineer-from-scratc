"""Review: the 'offline vs online correlation' in last quarter's eval review showed tau = 0.4 and everyone
concluded the offline eval was weak. Find the bug, fix it, explain:

WHY:
"""


def tau(x, y):
    n = len(x)
    s = 0
    for i in range(n):
        for j in range(i + 1, n):
            prod = (x[i] - x[j]) * (y[i] - y[j])
            s += (prod > 0) - (prod < 0)
    return s / (n * (n - 1) / 2)
