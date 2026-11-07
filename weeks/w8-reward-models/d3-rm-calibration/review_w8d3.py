"""Review: calibration dashboard. ECE jumps around wildly from week to week on a stable model.
Find the bug, fix it, explain:

WHY:
"""


def ece(probs, labels, n_bins=10):
    bins = [[] for _ in range(n_bins)]
    for p, y in zip(probs, labels):
        bins[min(int(p * n_bins), n_bins - 1)].append((p, y))
    gaps = []
    for b in bins:
        if b:
            conf = sum(p for p, _ in b) / len(b)
            acc = sum(y for _, y in b) / len(b)
            gaps.append(len(b) * abs(acc - conf))
    return sum(gaps) / len(probs)
