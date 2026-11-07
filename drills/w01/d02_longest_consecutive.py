"""d02 Longest consecutive sequence, O(n).
longest_consecutive([100, 4, 200, 1, 3, 2]) == 4   (1, 2, 3, 4)"""


def longest_consecutive(nums: list) -> int:
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best
