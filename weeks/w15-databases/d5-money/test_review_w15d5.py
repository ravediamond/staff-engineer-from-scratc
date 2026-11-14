import pytest

from review_w15d5 import Wallets


def test_review_amounts_are_integer_cents():
    w = Wallets()
    for _ in range(3):
        w.deposit("ana", 10)
    assert w.balance["ana"] == 30 and type(w.balance["ana"]) is int
    assert w.pay("ana", 30) is True and w.balance["ana"] == 0
    with pytest.raises(Exception):
        w.deposit("ana", 0.10)
    with pytest.raises(Exception):
        w.pay("ana", 0.30)
