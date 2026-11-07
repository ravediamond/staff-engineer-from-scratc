import random

from d05_most_water import max_area
from d06_longest_unique_substring import longest_unique
from d07_min_window import min_window
from d08_trapping_rain import trap


def test_d05():
    assert max_area([1, 8, 6, 2, 5, 4, 8, 3, 7]) == 49
    assert max_area([1, 1]) == 1
    rng = random.Random(0)
    for _ in range(50):
        h = [rng.randint(0, 10) for _ in range(rng.randint(2, 12))]
        assert max_area(h) == max((j - i) * min(h[i], h[j]) for i in range(len(h)) for j in range(i + 1, len(h)))


def test_d06():
    assert longest_unique("abcabcbb") == 3 and longest_unique("bbbbb") == 1
    assert longest_unique("pwwkew") == 3 and longest_unique("") == 0 and longest_unique("abba") == 2


def test_d07():
    assert min_window("ADOBECODEBANC", "ABC") == "BANC"
    assert min_window("a", "aa") == "" and min_window("aa", "aa") == "aa"
    assert min_window("abc", "") == ""


def test_d08():
    assert trap([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]) == 6
    assert trap([4, 2, 0, 3, 2, 5]) == 9 and trap([]) == 0
