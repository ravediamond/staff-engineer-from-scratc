import itertools

from d37_subsets import subsets
from d38_permutations import permutations
from d39_combination_sum import combination_sum
from d40_n_queens import total_n_queens


def test_d37():
    assert subsets([1, 2, 3]) == sorted([[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]])
    assert subsets([]) == [[]]


def test_d38():
    assert permutations([1, 1, 2]) == [[1, 1, 2], [1, 2, 1], [2, 1, 1]]
    assert permutations([1, 2, 3]) == sorted(list(p) for p in itertools.permutations([1, 2, 3]))


def test_d39():
    assert combination_sum([2, 3, 6, 7], 7) == [[2, 2, 3], [7]]
    assert combination_sum([2, 3, 5], 8) == [[2, 2, 2, 2], [2, 3, 3], [3, 5]]
    assert combination_sum([2], 1) == []


def test_d40():
    assert [total_n_queens(n) for n in range(1, 9)] == [1, 0, 0, 2, 10, 4, 40, 92]
