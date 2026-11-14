"""Review: range scan over the leaf level of a B+tree (used by "orders between two dates"). Reports are missing
orders, but only for date ranges that are "long enough". Find the bug, fix it, explain:

WHY:
"""


class Leaf:
    def __init__(self, keys, nxt=None):
        self.keys = keys
        self.next = nxt


def range_scan(first_leaf: Leaf, lo, hi) -> list:
    """first_leaf: the leaf where `lo` belongs. Return keys with lo <= key <= hi."""
    return [k for k in first_leaf.keys if lo <= k <= hi]
