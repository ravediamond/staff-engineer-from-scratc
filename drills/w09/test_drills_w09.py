import itertools
import random

from d33_unique_paths_obstacles import unique_paths
from d34_partition_equal import can_partition
from d35_jump_game_ii import jump
from d36_gas_station import can_complete


def test_d33():
    assert unique_paths([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == 2
    assert unique_paths([[0, 1], [0, 0]]) == 1 and unique_paths([[1]]) == 0


def test_d34():
    assert can_partition([1, 5, 11, 5]) and not can_partition([1, 2, 3, 5])
    rng = random.Random(0)
    for _ in range(50):
        a = [rng.randint(1, 9) for _ in range(rng.randint(1, 8))]
        brute = any(2 * sum(c) == sum(a) for r in range(len(a) + 1) for c in itertools.combinations(a, r))
        assert can_partition(a) == brute


def test_d35():
    assert jump([2, 3, 1, 1, 4]) == 2 and jump([2, 3, 0, 1, 4]) == 2 and jump([0]) == 0


def test_d36():
    assert can_complete([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert can_complete([2, 3, 4], [3, 4, 3]) == -1
