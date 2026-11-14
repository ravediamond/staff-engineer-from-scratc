"""Review: range scan over the leaf level of a B+tree.

WHY: the scan only looked at the first leaf. A range that crosses a leaf boundary must continue through
the `next` links until a key greater than `hi` is found. Short ranges usually fit in one leaf, which is
why the bug only showed on longer ones.
"""


class Leaf:
    def __init__(self, keys, nxt=None):
        self.keys = keys
        self.next = nxt


def range_scan(first_leaf: Leaf, lo, hi) -> list:
    out = []
    leaf = first_leaf
    while leaf is not None:
        for k in leaf.keys:
            if k > hi:
                return out
            if k >= lo:
                out.append(k)
        leaf = leaf.next
    return out
