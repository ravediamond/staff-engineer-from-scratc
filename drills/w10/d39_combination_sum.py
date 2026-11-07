"""d39 Combination sum: distinct positive candidates, each usable unlimited times; all combinations summing to target.
Return sorted list of sorted combinations."""


def combination_sum(candidates: list, target: int) -> list:
    cs = sorted(candidates)
    out = []

    def bt(start, remaining, cur):
        if remaining == 0:
            out.append(cur[:])
            return
        for i in range(start, len(cs)):
            if cs[i] > remaining:
                break
            cur.append(cs[i])
            bt(i, remaining - cs[i], cur)
            cur.pop()

    bt(0, target, [])
    return sorted(out)
