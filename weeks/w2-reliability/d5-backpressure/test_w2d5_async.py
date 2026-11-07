import asyncio
import time

import pytest

from w2d5_async import bounded_map, gather_settled, pipeline


def test_bounded_map_order_and_peak():
    async def fn(x):
        await asyncio.sleep(0.01 * (5 - x % 5))
        return x * x

    stats = {}
    t = time.perf_counter()
    out = asyncio.run(bounded_map(fn, list(range(40)), concurrency=8, stats=stats))
    assert out == [x * x for x in range(40)]
    assert stats["peak"] == 8
    assert time.perf_counter() - t < 1.0, "should overlap the sleeps"


def test_pipeline_results_and_backpressure():
    async def slow_double(x):
        await asyncio.sleep(0.002)
        return 2 * x

    async def inc(x):
        return x + 1

    stats = {}
    out = asyncio.run(pipeline(list(range(200)), [slow_double, inc], queue_size=5, workers_per_stage=3,
                               stats=stats))
    assert sorted(out) == [2 * x + 1 for x in range(200)]
    assert all(p <= 5 for p in stats["peak_q"]), f"queues exceeded maxsize: {stats['peak_q']}"


def test_pipeline_propagates_errors():
    async def bad(x):
        if x == 7:
            raise ValueError("item 7 is poison")
        await asyncio.sleep(0)
        return x

    with pytest.raises(ValueError, match="poison"):
        asyncio.run(asyncio.wait_for(pipeline(list(range(50)), [bad, bad], 4, 2), timeout=5))


def test_gather_settled():
    async def ok(v):
        return v

    async def ko():
        raise KeyError("x")

    out = asyncio.run(gather_settled([ok(1), ko(), ok(3)]))
    assert out[0] == ("ok", 1) and out[2] == ("ok", 3)
    assert out[1][0] == "err" and isinstance(out[1][1], KeyError)
