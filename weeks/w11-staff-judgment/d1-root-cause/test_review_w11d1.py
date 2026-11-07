from review_w11d1 import first_bad


def test_review_boundary():
    for bad in (1, 37, 99):
        assert first_bad(100, lambda i: i >= bad) == bad
