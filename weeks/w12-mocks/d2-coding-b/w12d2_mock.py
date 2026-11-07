"""W12 D2: coding mock B. Timer: 35 minutes for both."""
from collections import deque


def misra_gries(stream, k: int) -> dict:
    """At most k counters. Existing item: +1. New item with a free counter: set 1.
    New item with no free counter: decrement every counter, delete those reaching 0 (the new item is dropped)."""
    c: dict = {}
    for x in stream:
        if x in c:
            c[x] += 1
        elif len(c) < k:
            c[x] = 1
        else:
            for y in list(c):
                c[y] -= 1
                if c[y] == 0:
                    del c[y]
    return c


def ladder_length(begin: str, end: str, words: list) -> int:
    wordset = set(words)
    if end not in wordset:
        return 0
    q = deque([(begin, 1)])
    seen = {begin}
    while q:
        w, d = q.popleft()
        if w == end:
            return d
        for i in range(len(w)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nw = w[:i] + ch + w[i + 1:]
                if nw in wordset and nw not in seen:
                    seen.add(nw)
                    q.append((nw, d + 1))
    return 0
