"""d30 Longest palindromic substring (return the leftmost among the longest). O(n^2) expand-around-center is fine."""


def longest_palindrome(s: str) -> str:
    best = (0, 0)
    for c in range(len(s)):
        for lo, hi in ((c, c), (c, c + 1)):
            while lo >= 0 and hi < len(s) and s[lo] == s[hi]:
                lo, hi = lo - 1, hi + 1
            if hi - lo - 1 > best[1] - best[0]:
                best = (lo + 1, hi)
    return s[best[0]:best[1]]
