from review_w7d5 import tau


def test_review_perfect_agreement_is_one():
    assert tau([1, 2, 3, 4], [10, 20, 30, 40]) == 1.0
