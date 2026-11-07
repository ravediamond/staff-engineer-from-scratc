import pytest

from review_w2d3 import Conflict, Middleware


def test_review_key_reuse_with_new_body():
    m = Middleware()
    m.handle("k1", {"amount": 10}, lambda b: {"receipt": b["amount"]})
    assert m.handle("k1", {"amount": 10}, lambda b: {"receipt": -1}) == {"receipt": 10}
    with pytest.raises(Conflict):
        m.handle("k1", {"amount": 500}, lambda b: {"receipt": b["amount"]})
