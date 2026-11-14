import pytest

from review_w13d5 import relay


def test_review_crash_never_loses_an_event():
    rows = [{"id": 1, "topic": "orders.v1", "key": "o1", "payload": "{}"}]
    marked, sent = [], []

    def publish_crashing(topic, key, payload):
        raise RuntimeError("pod killed")

    with pytest.raises(RuntimeError):
        relay(rows, publish_crashing, marked.append)
    assert marked == [], "the row must still be unpublished so that the next run retries it"
    relay(rows, lambda t, k, p: sent.append(k), marked.append)
    assert sent == ["o1"] and marked == [1]
