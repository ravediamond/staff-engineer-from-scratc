"""W15 D2: a B+tree with splits and linked leaves, and index-usability rules."""
from bisect import bisect_left, bisect_right


class Node:
    def __init__(self, leaf: bool):
        self.leaf = leaf
        self.keys: list = []
        self.children: list = []     # internal nodes: len(children) == len(keys) + 1
        self.values: list = []       # leaves: values[i] belongs to keys[i]
        self.next = None             # leaves: the next leaf to the right


class BPlusTree:
    """order = maximum number of keys in a node. Child i of an internal node holds keys k with
    keys[i-1] <= k < keys[i]."""

    def __init__(self, order: int = 4):
        self.order = order
        self.root = Node(leaf=True)

    def _find_leaf(self, key) -> Node:
        """Walk from the root to the leaf that should contain key."""
        # TODO
        raise NotImplementedError

    def search(self, key):
        """The value stored for key, or None."""
        # TODO
        raise NotImplementedError

    def insert(self, key, value) -> None:
        """Insert or overwrite. If a node ends up with more than `order` keys, split it:
        - leaf: left keeps the first half (len // 2 keys), right gets the rest; the separator pushed up
          is the right half's first key (it STAYS in the leaf); fix the `next` links;
        - internal: the middle key (index len // 2) moves up and is in neither half.
        If the root splits, create a new root."""
        # TODO
        raise NotImplementedError

    def range(self, lo, hi) -> list:
        """All (key, value) with lo <= key <= hi, in key order: find lo's leaf, then follow `next` links."""
        # TODO
        raise NotImplementedError

    def height(self) -> int:
        """Number of levels (a single leaf = 1)."""
        # TODO
        raise NotImplementedError


def usable_prefix(index_cols: list[str], equality: set[str], range_col: str | None = None) -> int:
    """How many leading columns of a composite index narrow the scan for a query with equality predicates
    on `equality` and an optional range predicate on `range_col`. Walk the index columns in order:
    count each column that has an equality predicate; the first column without one counts only if it is
    the range column; then stop."""
    # TODO
    raise NotImplementedError


def is_covering(index_cols: list[str], include_cols: list[str], needed: set[str]) -> bool:
    """Index-only scan possible: every needed column is in the index key or its INCLUDE list."""
    # TODO
    raise NotImplementedError
