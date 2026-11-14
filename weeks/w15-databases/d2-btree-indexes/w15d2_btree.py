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
        node = self.root
        while not node.leaf:
            node = node.children[bisect_right(node.keys, key)]
        return node

    def search(self, key):
        """The value stored for key, or None."""
        leaf = self._find_leaf(key)
        i = bisect_left(leaf.keys, key)
        return leaf.values[i] if i < len(leaf.keys) and leaf.keys[i] == key else None

    def insert(self, key, value) -> None:
        """Insert or overwrite. If a node ends up with more than `order` keys, split it:
        - leaf: left keeps the first half (len // 2 keys), right gets the rest; the separator pushed up
          is the right half's first key (it STAYS in the leaf); fix the `next` links;
        - internal: the middle key (index len // 2) moves up and is in neither half.
        If the root splits, create a new root."""
        split = self._insert(self.root, key, value)
        if split is not None:
            sep, right = split
            new_root = Node(leaf=False)
            new_root.keys = [sep]
            new_root.children = [self.root, right]
            self.root = new_root

    def _insert(self, node: Node, key, value):
        if node.leaf:
            i = bisect_left(node.keys, key)
            if i < len(node.keys) and node.keys[i] == key:
                node.values[i] = value
                return None
            node.keys.insert(i, key)
            node.values.insert(i, value)
            if len(node.keys) <= self.order:
                return None
            mid = len(node.keys) // 2
            right = Node(leaf=True)
            right.keys, right.values = node.keys[mid:], node.values[mid:]
            node.keys, node.values = node.keys[:mid], node.values[:mid]
            right.next, node.next = node.next, right
            return right.keys[0], right
        i = bisect_right(node.keys, key)
        split = self._insert(node.children[i], key, value)
        if split is None:
            return None
        sep, child = split
        node.keys.insert(i, sep)
        node.children.insert(i + 1, child)
        if len(node.keys) <= self.order:
            return None
        mid = len(node.keys) // 2
        up = node.keys[mid]
        right = Node(leaf=False)
        right.keys, right.children = node.keys[mid + 1:], node.children[mid + 1:]
        node.keys, node.children = node.keys[:mid], node.children[:mid + 1]
        return up, right

    def range(self, lo, hi) -> list:
        """All (key, value) with lo <= key <= hi, in key order: find lo's leaf, then follow `next` links."""
        out = []
        leaf = self._find_leaf(lo)
        while leaf is not None:
            for k, v in zip(leaf.keys, leaf.values):
                if k > hi:
                    return out
                if k >= lo:
                    out.append((k, v))
            leaf = leaf.next
        return out

    def height(self) -> int:
        """Number of levels (a single leaf = 1)."""
        h, node = 1, self.root
        while not node.leaf:
            node = node.children[0]
            h += 1
        return h


def usable_prefix(index_cols: list[str], equality: set[str], range_col: str | None = None) -> int:
    """How many leading columns of a composite index narrow the scan for a query with equality predicates
    on `equality` and an optional range predicate on `range_col`. Walk the index columns in order:
    count each column that has an equality predicate; the first column without one counts only if it is
    the range column; then stop."""
    n = 0
    for col in index_cols:
        if col in equality:
            n += 1
        elif col == range_col:
            return n + 1
        else:
            return n
    return n


def is_covering(index_cols: list[str], include_cols: list[str], needed: set[str]) -> bool:
    """Index-only scan possible: every needed column is in the index key or its INCLUDE list."""
    return needed <= set(index_cols) | set(include_cols)
