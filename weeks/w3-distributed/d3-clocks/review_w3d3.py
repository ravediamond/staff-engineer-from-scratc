"""Review: vector clock merge in a replication layer. Concurrent updates started 'winning' silently.
Find the bug, fix it, explain:

WHY:
"""


def merge(a: dict, b: dict) -> dict:
    return dict(a) if sum(a.values()) >= sum(b.values()) else dict(b)
