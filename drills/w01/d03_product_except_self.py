"""d03 Product of array except self, O(n), no division.
product_except_self([1, 2, 3, 4]) == [24, 12, 8, 6]"""


def product_except_self(nums: list) -> list:
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):
        out[i] *= right
        right *= nums[i]
    return out
