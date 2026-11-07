"""Review: kappa from an internal dashboard. The judge looks 'substantial' on a skewed dataset where it is
basically saying "pass" to everything. Find the bug, fix it, explain:

WHY:
"""
from collections import Counter


def kappa(human, judge):
    n = len(human)
    po = sum(h == j for h, j in zip(human, judge)) / n
    ch, cj = Counter(human), Counter(judge)
    labels = set(human) | set(judge)
    pe = sum((ch[l] / n) ** 2 for l in labels)
    return (po - pe) / (1 - pe)
