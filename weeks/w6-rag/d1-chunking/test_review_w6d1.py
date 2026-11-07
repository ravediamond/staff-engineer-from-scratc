from review_w6d1 import windows


def test_review_no_gaps():
    s = windows("x" * 1000, 100, 20)
    covered = set()
    for a, b in s:
        covered |= set(range(a, b))
    assert covered == set(range(1000))
    assert s[1] == (80, 180)
