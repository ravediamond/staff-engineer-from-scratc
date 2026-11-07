from review_w12d2 import heavy_hitters


def test_review_zero_counters_removed():
    c = heavy_hitters("abcdefgha", 2)
    assert all(v > 0 for v in c.values())
    assert heavy_hitters("aabcc", 2) == {"a": 1, "c": 1}
