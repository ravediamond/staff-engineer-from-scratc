"""Review: a candidate's Misra-Gries. Memory grew without bound in their own load test. As the interviewer, find the
bug, fix it, and write your one-line feedback:

WHY:
"""


def heavy_hitters(stream, k):
    c = {}
    for x in stream:
        if x in c:
            c[x] += 1
        elif len(c) < k:
            c[x] = 1
        else:
            for y in list(c):
                c[y] -= 1
    return c
