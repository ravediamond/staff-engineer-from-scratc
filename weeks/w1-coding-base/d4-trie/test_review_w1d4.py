from review_w1d4 import Trie


def test_review_prefix_word_inserted_after():
    t = Trie()
    t.insert("cart")
    t.insert("car")
    assert t.contains("car") and t.contains("cart")
    assert not t.contains("ca")
