import asyncio

from review_w2d5 import backfill


def test_review_queue_is_bounded():
    assert asyncio.run(backfill(5000, maxsize=100)) <= 100
