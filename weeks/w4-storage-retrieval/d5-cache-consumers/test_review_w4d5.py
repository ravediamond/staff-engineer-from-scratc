import pytest

from review_w4d5 import Killed, consume


def test_review_no_message_lost():
    log = list(range(10))
    seen, state = set(), {"offset": 0}
    with pytest.raises(Killed):
        consume(log, state, seen.add, kill_at=4)
    consume(log, state, seen.add)
    assert seen == set(range(10))
