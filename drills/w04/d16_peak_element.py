"""d16 Find a peak element index (strictly greater than neighbours; nums[-1] = nums[n] = -inf). O(log n).
Adjacent elements are distinct. Any peak is accepted."""


def find_peak(nums: list) -> int:
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid
    return lo
