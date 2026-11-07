"""d21 Word search: does word exist in the grid as a path of horizontally/vertically adjacent cells, each used once?"""


def exist(board: list, word: str) -> bool:
    R, C = len(board), len(board[0]) if board else 0

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        ch, board[r][c] = board[r][c], "#"
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = ch
        return found

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
