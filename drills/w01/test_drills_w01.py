import random

from d01_group_anagrams import group_anagrams
from d02_longest_consecutive import longest_consecutive
from d03_product_except_self import product_except_self
from d04_subarray_sum_k import subarray_sum


def test_d01():
    assert group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"]) == [["ate", "eat", "tea"], ["bat"], ["nat", "tan"]]
    assert group_anagrams([]) == [] and group_anagrams([""]) == [[""]]


def test_d02():
    assert longest_consecutive([100, 4, 200, 1, 3, 2]) == 4
    assert longest_consecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]) == 9
    assert longest_consecutive([]) == 0


def test_d03():
    assert product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert product_except_self([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]


def test_d04():
    assert subarray_sum([1, 1, 1], 2) == 2
    assert subarray_sum([1, -1, 0], 0) == 3
    rng = random.Random(0)
    for _ in range(100):
        a = [rng.randint(-3, 3) for _ in range(rng.randint(0, 12))]
        k = rng.randint(-3, 3)
        brute = sum(sum(a[i:j]) == k for i in range(len(a)) for j in range(i + 1, len(a) + 1))
        assert subarray_sum(a, k) == brute
