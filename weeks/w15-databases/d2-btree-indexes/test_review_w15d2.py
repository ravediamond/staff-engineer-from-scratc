from review_w15d2 import Leaf, range_scan


def test_review_range_crosses_leaves():
    c = Leaf([9, 10, 12])
    b = Leaf([5, 6, 8], c)
    a = Leaf([1, 2, 3], b)
    assert range_scan(a, 2, 3) == [2, 3]
    assert range_scan(a, 2, 9) == [2, 3, 5, 6, 8, 9]
    assert range_scan(b, 6, 100) == [6, 8, 9, 10, 12]
