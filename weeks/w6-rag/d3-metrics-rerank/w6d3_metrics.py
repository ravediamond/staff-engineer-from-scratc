"""W6 D3: retrieval metrics, reranking, and bootstrap confidence intervals over queries."""
import math
import random


def recall_at_k(retrieved: list, relevant: set, k: int) -> float:
    """0.0 if relevant is empty."""
    if not relevant:
        return 0.0
    return len(set(retrieved[:k]) & relevant) / len(relevant)


def precision_at_k(retrieved: list, relevant: set, k: int) -> float:
    return len(set(retrieved[:k]) & relevant) / k


def reciprocal_rank(retrieved: list, relevant: set) -> float:
    for i, d in enumerate(retrieved, start=1):
        if d in relevant:
            return 1.0 / i
    return 0.0


def ndcg_at_k(retrieved: list, qrels: dict, k: int) -> float:
    """qrels: doc -> graded relevance (0, 1, 2, 3). Gain = 2^rel - 1, discount = log2(i + 1), i from 1.
    IDCG from the ideal ordering of ALL qrels. 0.0 if IDCG is 0."""
    dcg = sum((2 ** qrels.get(d, 0) - 1) / math.log2(i + 1) for i, d in enumerate(retrieved[:k], start=1))
    ideal = sorted(qrels.values(), reverse=True)[:k]
    idcg = sum((2 ** r - 1) / math.log2(i + 1) for i, r in enumerate(ideal, start=1))
    return dcg / idcg if idcg > 0 else 0.0


def rerank(candidates: list, scorer, k: int) -> list:
    """Rescore candidates with scorer(doc) -> float, return top-k by score desc. Stable for ties
    (keep the original order among equal scores)."""
    return sorted(candidates, key=lambda d: -scorer(d))[:k]


def bootstrap_ci(values: list, n_boot: int, seed: int, alpha: float = 0.05) -> tuple:
    """(mean, lo, hi): percentile bootstrap of the mean. Resample with random.Random(seed).choices.
    lo/hi = sorted bootstrap means at indices int(alpha/2 * n_boot) and int((1 - alpha/2) * n_boot) - 1."""
    rng = random.Random(seed)
    n = len(values)
    means = sorted(sum(rng.choices(values, k=n)) / n for _ in range(n_boot))
    return sum(values) / n, means[int(alpha / 2 * n_boot)], means[int((1 - alpha / 2) * n_boot) - 1]


def evaluate(run: dict, qrels: dict, k: int, n_boot: int = 1000, seed: int = 0) -> dict:
    """run: qid -> ranked doc list. qrels: qid -> {doc: grade}; relevant = grade > 0.
    Returns {"recall", "mrr", "ndcg"} -> (mean, lo, hi) over the qids in qrels (missing run = empty list)."""
    per = {"recall": [], "mrr": [], "ndcg": []}
    for qid, judg in qrels.items():
        got = run.get(qid, [])
        rel = {d for d, g in judg.items() if g > 0}
        per["recall"].append(recall_at_k(got, rel, k))
        per["mrr"].append(reciprocal_rank(got, rel))
        per["ndcg"].append(ndcg_at_k(got, judg, k))
    return {m: bootstrap_ci(v, n_boot, seed) for m, v in per.items()}
