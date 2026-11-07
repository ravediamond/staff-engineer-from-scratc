"""d29 House robber: max sum of non-adjacent values. O(n), O(1) space."""


def rob(nums: list) -> int:
    take = skip = 0  # best including / excluding the previous house
    for x in nums:
        take, skip = skip + x, max(take, skip)
    return max(take, skip)
