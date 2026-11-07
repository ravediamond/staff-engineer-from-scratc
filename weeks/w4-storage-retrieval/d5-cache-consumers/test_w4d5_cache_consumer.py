import asyncio

import pytest

from w4d5_cache_consumer import Consumer, Crash, SingleFlightCache, Sink


def test_single_flight_one_load_for_concurrent_misses():
    async def main():
        calls = []

        async def loader(k):
            calls.append(k)
            await asyncio.sleep(0.01)
            return k.upper()

        c = SingleFlightCache(loader, ttl=60, clock=lambda: 0)
        out = await asyncio.gather(*(c.get("a") for _ in range(100)), c.get("b"))
        assert out[:100] == ["A"] * 100 and out[100] == "B"
        assert c.loads == 2 and sorted(calls) == ["a", "b"]
        assert await c.get("a") == "A" and c.loads == 2

    asyncio.run(main())


def test_ttl_expiry_reloads():
    async def main():
        t = [0.0]

        async def loader(k):
            return t[0]

        c = SingleFlightCache(loader, ttl=10, clock=lambda: t[0])
        assert await c.get("k") == 0
        t[0] = 9
        assert await c.get("k") == 0
        t[0] = 10
        assert await c.get("k") == 10 and c.loads == 2

    asyncio.run(main())


def test_load_failure_propagates_and_is_not_cached():
    async def main():
        n = [0]

        async def loader(k):
            n[0] += 1
            await asyncio.sleep(0.01)
            if n[0] == 1:
                raise RuntimeError("db down")
            return "ok"

        c = SingleFlightCache(loader, ttl=60, clock=lambda: 0)
        res = await asyncio.gather(*(c.get("k") for _ in range(5)), return_exceptions=True)
        assert all(isinstance(r, RuntimeError) for r in res)
        assert await c.get("k") == "ok"

    asyncio.run(main())


def test_consumer_exactly_once_effect_across_crashes():
    log = [(f"m{i}", i) for i in range(1, 11)]
    sink = Sink()
    cons = Consumer(log, sink)
    with pytest.raises(Crash):
        cons.run(crash_after_effect_at=3)
    assert cons.committed == 3, "offset 3 had its effect but was not committed"
    with pytest.raises(Crash):
        cons.run(crash_after_effect_at=7)
    cons.run()
    assert sink.total == sum(range(1, 11)), "no loss, no duplicate"
    assert cons.committed == 10
