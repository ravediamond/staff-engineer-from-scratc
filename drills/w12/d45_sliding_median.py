"""d45 Sliding window median: medians of every window of size k (floats). O(n log k) with two heaps + lazy deletion,
or O(n k) with bisect.insort (accepted, but say the better approach)."""
import bisect


def median_sliding_window(nums: list, k: int) -> list:
    window = sorted(nums[:k])
    out = []

    def med():
        return float(window[k // 2]) if k % 2 else (window[k // 2 - 1] + window[k // 2]) / 2

    out.append(med())
    for i in range(k, len(nums)):
        window.pop(bisect.bisect_left(window, nums[i - k]))
        bisect.insort(window, nums[i])
        out.append(med())
    return out
