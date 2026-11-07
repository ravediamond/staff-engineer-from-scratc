from review_w12d1 import TimeMap


def test_review_exact_timestamp():
    t = TimeMap()
    t.set("k", "a", 10)
    t.set("k", "b", 20)
    assert t.get("k", 20) == "b"
    assert t.get("k", 15) == "a"
