from review_w6d3 import ndcg


def test_review_ideal_uses_all_judgments():
    grades = {"best": 3, "ok": 1}
    assert ndcg(["ok"], grades, 2) < 0.2
