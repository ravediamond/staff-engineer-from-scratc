import random
import statistics

from d13_rotated_search import search
from d14_min_eating_speed import min_speed
from d15_median_two_sorted import median
from d16_peak_element import find_peak


def test_d13():
    assert search([4, 5, 6, 7, 0, 1, 2], 0) == 4
    assert search([4, 5, 6, 7, 0, 1, 2], 3) == -1 and search([1], 0) == -1
    for k in range(7):
        arr = list(range(10, 17))
        arr = arr[k:] + arr[:k]
        for i, x in enumerate(arr):
            assert search(arr, x) == i


def test_d14():
    assert min_speed([3, 6, 7, 11], 8) == 4
    assert min_speed([30, 11, 23, 4, 20], 5) == 30
    assert min_speed([30, 11, 23, 4, 20], 6) == 23


def test_d15():
    assert median([1, 3], [2]) == 2.0 and median([1, 2], [3, 4]) == 2.5
    assert median([], [1]) == 1.0
    rng = random.Random(0)
    for _ in range(100):
        a = sorted(rng.randint(0, 50) for _ in range(rng.randint(0, 8)))
        b = sorted(rng.randint(0, 50) for _ in range(rng.randint(1, 8)))
        assert median(a, b) == statistics.median(a + b)


def test_d16():
    rng = random.Random(0)
    for _ in range(100):
        nums = rng.sample(range(100), rng.randint(1, 15))
        i = find_peak(nums)
        left = nums[i - 1] if i > 0 else float("-inf")
        right = nums[i + 1] if i < len(nums) - 1 else float("-inf")
        assert nums[i] > left and nums[i] > right
