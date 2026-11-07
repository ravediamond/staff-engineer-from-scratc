import pytest

from review_w12d5 import TransientError, call_with_retries


def test_review_real_bugs_not_retried():
    n = [0]

    def fn():
        n[0] += 1
        raise ValueError("real bug")

    with pytest.raises(ValueError):
        call_with_retries(fn, 3)
    assert n[0] == 1


def test_review_transient_retried():
    n = [0]

    def fn():
        n[0] += 1
        if n[0] < 3:
            raise TransientError()
        return "ok"

    assert call_with_retries(fn, 3) == ("ok", 3)
