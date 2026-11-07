"""d37 All subsets of distinct ints. Return sorted list of sorted subsets."""


def subsets(nums: list) -> list:
    out = []

    def bt(i, cur):
        if i == len(nums):
            out.append(sorted(cur))
            return
        bt(i + 1, cur)
        bt(i + 1, cur + [nums[i]])

    bt(0, [])
    return sorted(out)
