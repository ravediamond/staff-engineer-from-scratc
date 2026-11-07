import pytest

from review_w2d1 import HTTPError, call


def test_review_no_retry_on_client_error():
    n = [0]

    def fn():
        n[0] += 1
        raise HTTPError(400)

    with pytest.raises(HTTPError):
        call(fn, 4, lambda d: None, [0.1, 0.2, 0.4, 0.8])
    assert n[0] == 1, "a 400 fails the same way every time"


def test_review_retries_503():
    n = [0]

    def fn():
        n[0] += 1
        if n[0] < 3:
            raise HTTPError(503)
        return "ok"

    assert call(fn, 4, lambda d: None, [0.1, 0.2, 0.4, 0.8]) == "ok"
