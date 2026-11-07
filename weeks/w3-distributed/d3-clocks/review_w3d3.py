"""Review: vector clock merge in a replication layer. Concurrent updates started 'winning' silently.
Find the bug, fix it, explain:

WHY:
"""


def merge(a: dict, b: dict) -> dict:
    return {k: max(a.get(k, 0), b.get(k, 0)) for k in a.keys() | b.keys()}
