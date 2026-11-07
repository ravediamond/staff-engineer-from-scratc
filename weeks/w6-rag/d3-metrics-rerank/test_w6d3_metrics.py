import math

import pytest

from w6d3_metrics import bootstrap_ci, evaluate, ndcg_at_k, precision_at_k, recall_at_k, reciprocal_rank, rerank


def test_basic_metrics():
    rel, got = {"a", "b", "c"}, ["x", "a", "y", "b", "z"]
    assert recall_at_k(got, rel, 5) == pytest.approx(2 / 3)
    assert recall_at_k(got, rel, 1) == 0
    assert precision_at_k(got, rel, 5) == pytest.approx(0.4)
    assert reciprocal_rank(got, rel) == 0.5
    assert reciprocal_rank(["x"], rel) == 0.0
    assert recall_at_k(got, set(), 5) == 0.0


def test_ndcg_graded_and_ideal_from_qrels():
    qrels = {"a": 3, "b": 2, "c": 1}
    assert ndcg_at_k(["a", "b", "c"], qrels, 3) == pytest.approx(1.0)
    got = ["c", "x", "a"]
    dcg = 1 / math.log2(2) + 7 / math.log2(4)
    idcg = 7 / math.log2(2) + 3 / math.log2(3) + 1 / math.log2(4)
    assert ndcg_at_k(got, qrels, 3) == pytest.approx(dcg / idcg)
    assert ndcg_at_k(["c"], qrels, 1) < 0.2, "retrieving only the weakest doc is not 'perfect'"
    assert ndcg_at_k(["x"], {}, 1) == 0.0


def test_rerank_stable():
    scores = {"a": 0.1, "b": 0.9, "c": 0.9, "d": 0.5}
    assert rerank(["a", "b", "c", "d"], scores.get, 3) == ["b", "c", "d"]


def test_bootstrap_ci():
    m, lo, hi = bootstrap_ci([0.0, 1.0] * 50, n_boot=2000, seed=1)
    assert m == 0.5 and 0.38 < lo < 0.45 and 0.55 < hi < 0.62
    assert bootstrap_ci([0.7] * 10, 100, 0) == (pytest.approx(0.7), pytest.approx(0.7), pytest.approx(0.7))


def test_evaluate():
    qrels = {"q1": {"a": 1, "b": 0}, "q2": {"c": 2}, "q3": {"d": 1}}
    run = {"q1": ["a", "b"], "q2": ["x", "c"]}
    out = evaluate(run, qrels, k=2, n_boot=200, seed=0)
    assert out["recall"][0] == pytest.approx(2 / 3)
    assert out["mrr"][0] == pytest.approx((1 + 0.5 + 0) / 3)
    assert out["recall"][1] <= out["recall"][0] <= out["recall"][2]
