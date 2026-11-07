import random

from d09_daily_temperatures import daily_temperatures
from d10_largest_rectangle import largest_rectangle
from d11_eval_rpn import eval_rpn
from d12_decode_string import decode


def test_d09():
    assert daily_temperatures([73, 74, 75, 71, 69, 72, 76, 73]) == [1, 1, 4, 2, 1, 1, 0, 0]
    assert daily_temperatures([30, 30, 30]) == [0, 0, 0]


def test_d10():
    assert largest_rectangle([2, 1, 5, 6, 2, 3]) == 10
    assert largest_rectangle([2, 4]) == 4 and largest_rectangle([]) == 0
    rng = random.Random(0)
    for _ in range(50):
        h = [rng.randint(0, 6) for _ in range(rng.randint(1, 10))]
        brute = max(min(h[i:j + 1]) * (j - i + 1) for i in range(len(h)) for j in range(i, len(h)))
        assert largest_rectangle(h) == brute


def test_d11():
    assert eval_rpn(["2", "1", "+", "3", "*"]) == 9
    assert eval_rpn(["4", "13", "5", "/", "+"]) == 6
    assert eval_rpn(["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]) == 22


def test_d12():
    assert decode("3[a2[c]]") == "accaccacc"
    assert decode("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert decode("10[a]") == "a" * 10 and decode("abc") == "abc"
