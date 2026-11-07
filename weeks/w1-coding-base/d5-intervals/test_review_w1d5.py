from review_w1d5 import merge


def test_review_containing_interval():
    assert merge([[1, 3], [2, 6], [8, 10]]) == [[1, 6], [8, 10]]
    assert merge([[2, 3], [4, 5], [1, 10]]) == [[1, 10]]
