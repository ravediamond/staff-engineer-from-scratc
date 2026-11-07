"""Review: a fusion function. Results look dominated by whichever retriever has bigger raw scores.
Find the bug, fix it, explain:

WHY:
"""
from collections import defaultdict


def rrf(results, k=60):
    """results: list of lists of (doc_id, score), each best first."""
    fused = defaultdict(float)
    for lst in results:
        for rank, (doc, score) in enumerate(lst, start=1):
            fused[doc] += 1.0 / (k + rank)
    return sorted(fused, key=lambda d: (-fused[d], d))
