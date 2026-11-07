from review_w5d4 import Receipts


def test_review_out_of_order_acks():
    r = Receipts()
    for s in (3, 10, 6):
        r.ack("ana", "g", s)
    assert r.unread("ana", "g", 10) == 0
