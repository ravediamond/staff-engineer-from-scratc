import random

from d17_merge_k_sorted import merge_k
from d18_kth_largest_stream import KthLargest
from d19_employee_free_time import free_time
from d20_max_capital import max_capital


def test_d17():
    assert merge_k([[1, 4, 5], [1, 3, 4], [2, 6]]) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert merge_k([]) == [] and merge_k([[], [1]]) == [1]


def test_d18():
    k = KthLargest(3, [4, 5, 8, 2])
    assert [k.add(x) for x in [3, 5, 10, 9, 4]] == [4, 5, 5, 8, 8]
    k2 = KthLargest(1, [])
    assert k2.add(-3) == -3 and k2.add(-2) == -2


def test_d19():
    assert free_time([[[1, 2], [5, 6]], [[1, 3]], [[4, 10]]]) == [[3, 4]]
    assert free_time([[[1, 3], [6, 7]], [[2, 4]], [[2, 5], [9, 12]]]) == [[5, 6], [7, 9]]
    assert free_time([[[1, 2]], [[2, 3]]]) == []


def test_d20():
    assert max_capital(2, 0, [1, 2, 3], [0, 1, 1]) == 4
    assert max_capital(3, 0, [1, 2, 3], [0, 1, 2]) == 6
    assert max_capital(1, 0, [5], [1]) == 0
