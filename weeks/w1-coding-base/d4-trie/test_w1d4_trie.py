from w1d4_trie import Trie


def test_contains_vs_prefix():
    t = Trie()
    for w in ["cart", "care", "dog"]:
        t.insert(w)
    assert t.contains("cart") and not t.contains("car")
    assert t.starts_with("car") and not t.starts_with("cat")
    t.insert("car")
    assert t.contains("car")
    assert t.starts_with("")


def test_node_count():
    t = Trie()
    for w in ["car", "cart", "care", "dog"]:
        t.insert(w)
    assert t.node_count() == 1 + 3 + 1 + 1 + 3


def test_delete_prunes():
    t = Trie()
    for w in ["car", "cart", "dog"]:
        t.insert(w)
    before = t.node_count()
    assert t.delete("car") is True
    assert t.node_count() == before, "cart still needs the c-a-r path"
    assert not t.contains("car") and t.contains("cart")
    assert t.delete("cart") is True
    assert t.node_count() == 1 + 3, "only d-o-g left"
    assert t.delete("cart") is False
    assert t.delete("do") is False


def test_top_k_order():
    t = Trie()
    data = {"apple": 5, "app": 9, "application": 5, "apply": 2, "banana": 50, "ape": 5}
    for w, c in data.items():
        t.insert(w, c)
    t.insert("apply", 1)
    assert t.top_k("ap", 4) == ["app", "ape", "apple", "application"]
    assert t.top_k("appl", 10) == ["apple", "application", "apply"]
    assert t.top_k("z", 3) == []
    assert t.top_k("", 1) == ["banana"]
