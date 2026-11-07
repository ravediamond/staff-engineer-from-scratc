from review_w1d3 import LRU


def test_review_get_refreshes():
    c = LRU(2)
    c.put("a", 1)
    c.put("b", 2)
    c.get("a")
    c.put("c", 3)
    assert c.get("a") == 1, "a was just read; b should have been evicted"
    assert c.get("b") is None
