"""d28 Serialize a binary tree to a string and back. Any format; deserialize(serialize(t)) must equal t."""
from d25_level_order import TreeNode, build  # noqa: F401


def serialize(root) -> str:
    out = []

    def pre(n):
        if n is None:
            out.append("#")
            return
        out.append(str(n.val))
        pre(n.left)
        pre(n.right)

    pre(root)
    return ",".join(out)


def deserialize(s: str):
    it = iter(s.split(","))

    def build_():
        v = next(it)
        if v == "#":
            return None
        n = TreeNode(int(v))
        n.left = build_()
        n.right = build_()
        return n

    return build_()
