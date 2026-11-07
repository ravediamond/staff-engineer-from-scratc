"""W6 D3: retrieval metrics, reranking, and bootstrap confidence intervals over queries."""
import math
import random


def recall_at_k(retrieved: list, relevant: set, k: int) -> float:
    """0.0 if relevant is empty."""
    # TODO
    raise NotImplementedError


def precision_at_k(retrieved: list, relevant: set, k: int) -> float:
    # TODO
    raise NotImplementedError


def reciprocal_rank(retrieved: list, relevant: set) -> float:
    # TODO
    raise NotImplementedError


def ndcg_at_k(retrieved: list, qrels: dict, k: int) -> float:
    """qrels: doc -> graded relevance (0, 1, 2, 3). Gain = 2^rel - 1, discount = log2(i + 1), i from 1.
    IDCG from the ideal ordering of ALL qrels. 0.0 if IDCG is 0."""
    # TODO
    raise NotImplementedError


def rerank(candidates: list, scorer, k: int) -> list:
    """Rescore candidates with scorer(doc) -> float, return top-k by score desc. Stable for ties
    (keep the original order among equal scores)."""
    # TODO
    raise NotImplementedError


def bootstrap_ci(values: list, n_boot: int, seed: int, alpha: float = 0.05) -> tuple:
    """(mean, lo, hi): percentile bootstrap of the mean. Resample with random.Random(seed).choices.
    lo/hi = sorted bootstrap means at indices int(alpha/2 * n_boot) and int((1 - alpha/2) * n_boot) - 1."""
    # TODO
    raise NotImplementedError


def evaluate(run: dict, qrels: dict, k: int, n_boot: int = 1000, seed: int = 0) -> dict:
    """run: qid -> ranked doc list. qrels: qid -> {doc: grade}; relevant = grade > 0.
    Returns {"recall", "mrr", "ndcg"} -> (mean, lo, hi) over the qids in qrels (missing run = empty list)."""
    # TODO
    raise NotImplementedError
