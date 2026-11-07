import random
import re
import statistics

from d45_sliding_median import median_sliding_window
from d46_regex_matching import is_match
from d47_longest_increasing_path import longest_increasing_path
from d48_text_justification import justify


def test_d45():
    assert median_sliding_window([1, 3, -1, -3, 5, 3, 6, 7], 3) == [1.0, -1.0, -1.0, 3.0, 5.0, 6.0]
    rng = random.Random(0)
    a = [rng.randint(-5, 5) for _ in range(30)]
    assert median_sliding_window(a, 4) == [statistics.median(a[i:i + 4]) for i in range(27)]


def test_d46():
    cases = [("aa", "a"), ("aa", "a*"), ("ab", ".*"), ("aab", "c*a*b"), ("mississippi", "mis*is*p*."), ("", "a*b*")]
    for s, p in cases:
        assert is_match(s, p) == bool(re.fullmatch(p, s)), (s, p)


def test_d47():
    assert longest_increasing_path([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4
    assert longest_increasing_path([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4
    assert longest_increasing_path([[1]]) == 1


def test_d48():
    assert justify(["This", "is", "an", "example", "of", "text", "justification."], 16) == [
        "This    is    an", "example  of text", "justification.  "]
    assert justify(["What", "must", "be", "acknowledgment", "shall", "be"], 16) == [
        "What   must   be", "acknowledgment  ", "shall be        "]
