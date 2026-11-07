from d25_level_order import build, level_order
from d26_validate_bst import is_bst
from d27_lca import lca
from d28_serialize_tree import deserialize, serialize


def test_d25():
    assert level_order(build([3, 9, 20, None, None, 15, 7])) == [[3], [9, 20], [15, 7]]
    assert level_order(None) == []


def test_d26():
    assert is_bst(build([2, 1, 3]))
    assert not is_bst(build([5, 1, 4, None, None, 3, 6]))
    assert not is_bst(build([5, 4, 6, None, None, 3, 7])), "3 is in the right subtree of 5"
    assert not is_bst(build([1, 1]))


def test_d27():
    t = build([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4])
    assert lca(t, 5, 1) == 3 and lca(t, 5, 4) == 5 and lca(t, 7, 8) == 3


def test_d28():
    for vals in ([1, 2, 3, None, None, 4, 5], [], [1], [1, None, 2, None, 3], [-1, 0, 1]):
        t = build(vals)
        assert level_order(deserialize(serialize(t))) == level_order(t)
