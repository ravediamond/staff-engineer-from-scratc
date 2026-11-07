from review_w5d2 import make_id


def test_review_fields_do_not_overlap():
    ids = {make_id(1, w, s) for w in range(0, 1024, 7) for s in range(0, 4096, 13)}
    assert len(ids) == len(range(0, 1024, 7)) * len(range(0, 4096, 13))
    assert make_id(0, 1, 0) == 4096
