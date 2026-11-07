"""d34 Partition equal subset sum: can nums (positive ints) be split into two subsets of equal sum?"""


def can_partition(nums: list) -> bool:
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    reach = 1  # bitset of reachable sums
    for x in nums:
        reach |= reach << x
    return bool(reach >> target & 1)
