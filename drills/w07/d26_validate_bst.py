"""d26 Validate a binary search tree (strict: left < node < right for all descendants)."""
from d25_level_order import TreeNode, build  # noqa: F401  (shared helpers)


def is_bst(root) -> bool:
    def ok(n, lo, hi):
        if n is None:
            return True
        if not (lo < n.val < hi):
            return False
        return ok(n.left, lo, n.val) and ok(n.right, n.val, hi)

    return ok(root, float("-inf"), float("inf"))
