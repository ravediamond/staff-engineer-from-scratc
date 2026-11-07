from review_w5d3 import merge_feeds


def test_review_newest_first():
    a = [(9, "a9"), (5, "a5"), (1, "a1")]
    b = [(8, "b8"), (2, "b2")]
    assert merge_feeds([a, b], 3) == ["a9", "b8", "a5"]
