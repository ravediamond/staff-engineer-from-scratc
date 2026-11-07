"""d06 Length of the longest substring without repeating characters. O(n).
longest_unique("abcabcbb") == 3"""


def longest_unique(s: str) -> int:
    last, start, best = {}, 0, 0
    for i, ch in enumerate(s):
        if ch in last and last[ch] >= start:
            start = last[ch] + 1
        last[ch] = i
        best = max(best, i - start + 1)
    return best
