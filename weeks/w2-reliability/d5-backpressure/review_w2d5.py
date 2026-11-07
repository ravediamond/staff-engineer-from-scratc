"""Review: an embedding backfill job. Worked on 10k docs. OOM-killed on 50M docs.
Find the bug, fix it, explain:

WHY:
"""
import asyncio


async def backfill(n_items: int, maxsize: int) -> int:
    """Fast producer, slow consumer. Returns the peak queue size observed."""
    q = asyncio.Queue(maxsize=maxsize)
    peak = 0

    async def consumer():
        for _ in range(n_items):
            await q.get()
            await asyncio.sleep(0)

    c = asyncio.create_task(consumer())
    for i in range(n_items):
        await q.put(i)
        peak = max(peak, q.qsize())
    await c
    return peak
