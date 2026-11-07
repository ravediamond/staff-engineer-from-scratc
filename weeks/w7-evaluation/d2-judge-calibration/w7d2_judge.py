"""W7 D2: agreement statistics and position-bias checks for LLM judges."""
from collections import Counter


def confusion(a: list, b: list, labels: list) -> list:
    """Matrix m[i][j] = count of items where a == labels[i] and b == labels[j]."""
    idx = {l: i for i, l in enumerate(labels)}
    m = [[0] * len(labels) for _ in labels]
    for x, y in zip(a, b):
        m[idx[x]][idx[y]] += 1
    return m


def cohen_kappa(a: list, b: list) -> float:
    """(p_o - p_e) / (1 - p_e). If p_e == 1 (both raters constant and identical) return 1.0."""
    n = len(a)
    po = sum(x == y for x, y in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[l] / n * cb[l] / n for l in set(a) | set(b))
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def weighted_kappa(a: list, b: list, labels: list) -> float:
    """Quadratic weights w_ij = (i - j)^2 / (k - 1)^2 over the ordered labels.
    kappa_w = 1 - sum(w * observed) / sum(w * expected), expected from the outer product of marginals."""
    k, n = len(labels), len(a)
    obs = confusion(a, b, labels)
    ra = [sum(row) for row in obs]
    rb = [sum(obs[i][j] for i in range(k)) for j in range(k)]
    num = den = 0.0
    for i in range(k):
        for j in range(k):
            w = (i - j) ** 2 / (k - 1) ** 2
            num += w * obs[i][j]
            den += w * ra[i] * rb[j] / n
    return 1.0 if den == 0 else 1 - num / den


def position_consistency(ab: list, ba: list) -> float:
    """ab[i]: judge's pick ("A"|"B"|"tie") when shown (A, B); ba[i]: pick when shown (B, A), expressed in
    the SAME labels (i.e. "A" still means answer A). Consistent = same pick in both orders. Return the rate."""
    return sum(x == y for x, y in zip(ab, ba)) / len(ab)


def debiased_verdicts(ab: list, ba: list) -> list:
    """Per item: the pick if both orders agree, else "tie"."""
    return [x if x == y else "tie" for x, y in zip(ab, ba)]
