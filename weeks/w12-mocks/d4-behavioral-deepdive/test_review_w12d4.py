from review_w12d4 import panel_score


def test_review_weights_normalized():
    assert panel_score({"a": 3, "b": 3}, {"a": 1, "b": 1}) == 3
    assert panel_score({"a": 3, "b": 3, "c": 3}, {"a": 2, "b": 1, "c": 1}) == 3
