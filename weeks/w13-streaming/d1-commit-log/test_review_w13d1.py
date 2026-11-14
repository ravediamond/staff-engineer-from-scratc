from review_w13d1 import compact


def test_review_offsets_survive_compaction():
    recs = [(0, "a", 1), (1, "b", 2), (2, "a", 3), (3, "b", None), (4, "c", 5)]
    assert compact(recs) == [(2, "a", 3), (4, "c", 5)]
