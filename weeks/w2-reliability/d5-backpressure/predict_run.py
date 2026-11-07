"""Self-contained. Run after predict.md (takes ~25 s)."""
import asyncio
import time


async def main():
    t = time.perf_counter()
    await asyncio.gather(*(asyncio.sleep(1) for _ in range(1000)))
    print(f"1. 1000 sleeps, no limit: {time.perf_counter() - t:.2f} s")
    sem = asyncio.Semaphore(50)

    async def limited():
        async with sem:
            await asyncio.sleep(1)

    t = time.perf_counter()
    await asyncio.gather(*(limited() for _ in range(1000)))
    print(f"2. Semaphore(50): {time.perf_counter() - t:.2f} s (1000 / 50 x 1 s)")
    q, peak = asyncio.Queue(), 0

    async def consumer():
        while True:
            await q.get()
            await asyncio.sleep(0.001)
            q.task_done()

    c = asyncio.create_task(consumer())
    for i in range(10_000):
        await q.put(i)
        peak = max(peak, q.qsize())
    print(f"3. unbounded queue peak: {peak} (put never waits)")
    c.cancel()
    print("4. Little's law: 50 req/s x 4 s = 200 in flight")


asyncio.run(main())
