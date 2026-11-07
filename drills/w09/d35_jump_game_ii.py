"""d35 Jump game II: nums[i] = max jump from i. Minimum jumps to reach the last index (always reachable). Greedy O(n)."""


def jump(nums: list) -> int:
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
