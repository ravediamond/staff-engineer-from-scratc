from review_w4d1 import TOMB, lsm_get


def test_review_newest_first():
    ssts = [{"k": "v3"}, {"k": "v2"}, {"k": "v1"}]
    assert lsm_get({}, ssts, "k") == "v3"
    assert lsm_get({}, [{"k": TOMB}, {"k": "v1"}], "k") is None
