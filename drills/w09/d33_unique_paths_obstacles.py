"""d33 Unique paths from top-left to bottom-right moving right/down; 1 = obstacle. O(m*n) time, O(n) space."""


def unique_paths(grid: list) -> int:
    n = len(grid[0])
    dp = [0] * n
    dp[0] = 1 if grid[0][0] == 0 else 0
    for row in grid:
        for j in range(n):
            if row[j] == 1:
                dp[j] = 0
            elif j > 0:
                dp[j] += dp[j - 1]
    return dp[-1]
