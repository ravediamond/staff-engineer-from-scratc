"""Review: leader commit logic. Passed all happy-path tests. A chaos test found a committed entry that later
disappeared after two leader changes. Find the bug, fix it, explain:

WHY:
"""


def advance_commit(log, current_term, commit_index, match_indexes):
    """log: list of (term, cmd), 1-indexed. match_indexes: followers only. Leader counts itself."""
    cluster = len(match_indexes) + 1
    for n in range(len(log), commit_index, -1):
        votes = 1 + sum(m >= n for m in match_indexes)
        if votes * 2 > cluster:
            return n
    return commit_index
