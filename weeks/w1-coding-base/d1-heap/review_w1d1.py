"""Review: this pop looks right and passes a quick manual check. It is wrong.
Find the bug, fix it, and write one line here explaining it:

WHY:
"""


def heap_push(h: list, x) -> None:
    h.append(x)
    i = len(h) - 1
    while i > 0 and h[(i - 1) // 2] > h[i]:
        p = (i - 1) // 2
        h[i], h[p] = h[p], h[i]
        i = p


def heap_pop(h: list):
    last = h.pop()
    if not h:
        return last
    top, h[0] = h[0], last
    i, n = 0, len(h)
    while True:
        l, r = 2 * i + 1, 2 * i + 2
        if l >= n:
            break
        child = r if (r < n and h[r] < h[l]) else l
        if h[child] < h[i]:
            h[i], h[child] = h[child], h[i]
            i = child
        else:
            break
    return top
