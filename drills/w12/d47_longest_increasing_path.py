"""d47 Longest strictly increasing path in a matrix (4-directional). DFS + memoisation."""
from functools import lru_cache


def longest_increasing_path(matrix: list) -> int:
    if not matrix:
        return 0
    R, C = len(matrix), len(matrix[0])

    @lru_cache(maxsize=None)
    def dfs(r, c):
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        return best

    return max(dfs(r, c) for r in range(R) for c in range(C))
