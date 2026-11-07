from d29_house_robber import rob
from d30_longest_palindrome import longest_palindrome
from d31_word_break import word_break
from d32_decode_ways import num_decodings


def test_d29():
    assert rob([1, 2, 3, 1]) == 4 and rob([2, 7, 9, 3, 1]) == 12 and rob([]) == 0 and rob([5]) == 5


def test_d30():
    assert longest_palindrome("babad") == "bab"
    assert longest_palindrome("cbbd") == "bb" and longest_palindrome("a") == "a" and longest_palindrome("") == ""


def test_d31():
    assert word_break("leetcode", ["leet", "code"])
    assert word_break("applepenapple", ["apple", "pen"])
    assert not word_break("catsandog", ["cats", "dog", "sand", "and", "cat"])


def test_d32():
    assert num_decodings("12") == 2 and num_decodings("226") == 3
    assert num_decodings("06") == 0 and num_decodings("10") == 1 and num_decodings("2101") == 1
