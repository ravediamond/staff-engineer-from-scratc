"""d04 Number of contiguous subarrays summing to k (values may be negative). O(n).
subarray_sum([1, 1, 1], 2) == 2"""
from collections import defaultdict


def subarray_sum(nums: list, k: int) -> int:
    seen = defaultdict(int)
    seen[0] = 1
    s = count = 0
    for x in nums:
        s += x
        count += seen[s - k]
        seen[s] += 1
    return count
