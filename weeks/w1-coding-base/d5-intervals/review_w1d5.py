"""Review: interval merge from a code review. Passes the example in the docstring. Find the bug, fix, explain:

WHY:
"""


def merge(intervals):
    """merge([[1,3],[2,6],[8,10]]) == [[1,6],[8,10]]"""
    intervals = sorted(intervals, key=lambda iv: iv[1])
    out = []
    for s, e in intervals:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
