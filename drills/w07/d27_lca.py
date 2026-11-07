"""d27 Lowest common ancestor of two values p, q in a binary tree (not necessarily a BST). Both exist. Return the value."""
from d25_level_order import TreeNode, build  # noqa: F401


def lca(root, p, q):
    def go(n):
        if n is None or n.val in (p, q):
            return n
        l, r = go(n.left), go(n.right)
        if l and r:
            return n
        return l or r

    return go(root).val
