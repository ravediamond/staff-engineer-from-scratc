"""Review: a shrinker in the team's test helpers. Failing property tests print huge, unreadable inputs.
Find the bug, fix it, explain:

WHY:
"""


def minimize(x, fails, shrinker):
    current = x
    progress = True
    while progress:
        progress = False
        for cand in shrinker(current):
            if fails(cand):
                current = cand
                progress = True
                break
    return current
