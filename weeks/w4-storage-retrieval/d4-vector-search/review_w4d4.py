"""Review: retrieval service. The same three boilerplate chunks come back for every query.
Find the bug, fix it, explain:

WHY:
"""
import numpy as np


def top_k_cosine(X, q, k):
    Xn = X / np.linalg.norm(X, axis=1, keepdims=True)
    sims = Xn @ (q / np.linalg.norm(q))
    return np.argsort(-sims)[:k].tolist()
