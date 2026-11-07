from review_w3d3 import merge


def test_review_elementwise_max():
    assert merge({"a": 3, "b": 0}, {"a": 0, "b": 1}) == {"a": 3, "b": 1}
    assert merge({"a": 1}, {"c": 5}) == {"a": 1, "c": 5}
