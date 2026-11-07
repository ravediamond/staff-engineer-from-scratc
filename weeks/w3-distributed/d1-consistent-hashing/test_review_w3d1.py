from review_w3d1 import Ring, h


def test_review_keys_past_last_point():
    r = Ring(["a", "b", "c"], vnodes=2)
    past_end = [k for k in (f"key{i}" for i in range(5000)) if h(k) > r.hashes[-1]]
    assert past_end, "test setup: need keys beyond the last point"
    for k in past_end:
        assert r.lookup(k) == r.nodes[0]
