"""d38 All permutations of possibly-duplicated ints, without duplicate permutations. Return sorted."""


def permutations(nums: list) -> list:
    nums = sorted(nums)
    out, used = [], [False] * len(nums)

    def bt(cur):
        if len(cur) == len(nums):
            out.append(cur[:])
            return
        for i in range(len(nums)):
            if used[i] or (i > 0 and nums[i] == nums[i - 1] and not used[i - 1]):
                continue
            used[i] = True
            cur.append(nums[i])
            bt(cur)
            cur.pop()
            used[i] = False

    bt([])
    return out
