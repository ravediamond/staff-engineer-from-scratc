from review_w6d2 import rrf


def test_review_ranks_not_scores():
    bm25 = [("a", 42.0), ("b", 30.0)]
    dense = [("c", 0.9), ("a", 0.5)]
    assert rrf([bm25, dense]) == ["a", "c", "b"], "c is rank 1 in dense; small raw scores must not bury it"
