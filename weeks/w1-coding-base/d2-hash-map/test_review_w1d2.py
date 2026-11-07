from review_w1d2 import TinyMap


class K:
    def __init__(self, v):
        self.v = v

    def __hash__(self):
        return 3

    def __eq__(self, o):
        return isinstance(o, K) and o.v == self.v


def test_review_delete_middle_of_chain():
    m = TinyMap()
    a, b, c = K(1), K(2), K(3)
    m.put(a, "a")
    m.put(b, "b")
    m.put(c, "c")
    m.delete(b)
    assert m.get(c) == "c"
