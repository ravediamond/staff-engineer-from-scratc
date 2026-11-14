import schema
from review_w15d3 import INACTIVE_USERS


def test_review_inactive_users_despite_guest_orders():
    assert schema.connect().execute(INACTIVE_USERS).fetchall() == [("ed",)]
