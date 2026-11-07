"""Review: nDCG from an internal eval library. Every system scores 0.97+ and nobody can tell them apart.
Find the bug, fix it, explain:

WHY:
"""
import math


def ndcg(retrieved, grades, k):
    gains = [2 ** grades.get(d, 0) - 1 for d in retrieved[:k]]
    dcg = sum(g / math.log2(i + 2) for i, g in enumerate(gains))
    ideal = sorted((2 ** g - 1 for g in grades.values()), reverse=True)[:k]
    idcg = sum(g / math.log2(i + 2) for i, g in enumerate(ideal))
    return dcg / idcg if idcg else 0.0
