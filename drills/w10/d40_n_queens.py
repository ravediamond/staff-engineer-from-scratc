"""d40 Number of ways to place n non-attacking queens on an n x n board."""


def total_n_queens(n: int) -> int:
    count = 0

    def bt(r, cols, d1, d2):
        nonlocal count
        if r == n:
            count += 1
            return
        for c in range(n):
            if c in cols or r - c in d1 or r + c in d2:
                continue
            bt(r + 1, cols | {c}, d1 | {r - c}, d2 | {r + c})

    bt(0, frozenset(), frozenset(), frozenset())
    return count
