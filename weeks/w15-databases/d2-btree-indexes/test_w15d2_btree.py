import random

from w15d2_btree import BPlusTree, is_covering, usable_prefix


def check_invariants(tree):
    depths = set()

    def walk(node, depth, lo, hi):
        assert node.keys == sorted(node.keys) and len(node.keys) <= tree.order
        for k in node.keys:
            assert (lo is None or k >= lo) and (hi is None or k < hi)
        if node.leaf:
            depths.add(depth)
            assert len(node.values) == len(node.keys)
            return
        assert len(node.children) == len(node.keys) + 1
        bounds = [lo, *node.keys, hi]
        for i, child in enumerate(node.children):
            walk(child, depth + 1, bounds[i], bounds[i + 1])

    walk(tree.root, 1, None, None)
    assert len(depths) == 1, "all leaves at the same depth"


def test_first_split():
    t = BPlusTree(order=4)
    for k in range(1, 6):
        t.insert(k, k * 10)
    assert not t.root.leaf and t.root.keys == [3]
    left, right = t.root.children
    assert left.keys == [1, 2] and right.keys == [3, 4, 5] and left.next is right
    assert t.height() == 2


def test_insert_search_random_order():
    rng = random.Random(0)
    keys = list(range(2000))
    rng.shuffle(keys)
    t = BPlusTree(order=8)
    for k in keys:
        t.insert(k, str(k))
    check_invariants(t)
    assert all(t.search(k) == str(k) for k in range(0, 2000, 37))
    assert t.search(-1) is None and t.search(2000) is None
    assert t.height() <= 6, "height grows with log(n)"
    t.insert(5, "new")
    assert t.search(5) == "new"


def test_sequential_inserts_keep_balance():
    t = BPlusTree(order=4)
    for k in range(500):
        t.insert(k, k)
    check_invariants(t)
    assert t.search(499) == 499


def test_range_follows_leaf_links():
    t = BPlusTree(order=4)
    for k in range(0, 200, 2):
        t.insert(k, k)
    assert t.range(10, 31) == [(k, k) for k in range(10, 32, 2)]
    assert t.range(-5, 3) == [(0, 0), (2, 2)]
    assert t.range(197, 500) == [(198, 198)]
    assert t.range(51, 51) == []
    assert len(t.range(0, 198)) == 100


def test_usable_prefix():
    idx = ["tenant_id", "created_at", "status"]
    assert usable_prefix(idx, {"tenant_id", "status"}) == 1
    assert usable_prefix(idx, {"tenant_id", "status"}, "created_at") == 2
    assert usable_prefix(idx, set(), "created_at") == 0
    assert usable_prefix(idx, {"tenant_id", "created_at", "status"}) == 3
    assert usable_prefix(["tenant_id", "status", "created_at"], {"tenant_id", "status"}, "created_at") == 3
    assert usable_prefix(idx, {"tenant_id"}, "tenant_id") == 1


def test_covering():
    assert is_covering(["tenant_id", "created_at"], ["status"], {"tenant_id", "status"})
    assert not is_covering(["tenant_id", "created_at"], [], {"tenant_id", "status"})
