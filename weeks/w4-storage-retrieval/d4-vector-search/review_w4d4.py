"""Review: retrieval service. The same three boilerplate chunks come back for every query.
Find the bug, fix it, explain:

WHY:
"""
import numpy as np


def top_k_cosine(X, q, k):
    sims = X @ q
    return np.argsort(-sims)[:k].tolist()
