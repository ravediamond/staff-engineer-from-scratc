"""W2 D5: bounded concurrency, multi-stage pipeline with backpressure, settled gather."""
import asyncio

_STOP = object()


async def bounded_map(fn, items: list, concurrency: int, stats: dict | None = None) -> list:
    """await fn(item) for every item, at most `concurrency` at once. Results in input order.
    If stats is given, set stats["peak"] to the max number of fn calls in flight."""
    sem = asyncio.Semaphore(concurrency)
    in_flight = 0
    peak = 0

    async def run(x):
        nonlocal in_flight, peak
        async with sem:
            in_flight += 1
            peak = max(peak, in_flight)
            try:
                return await fn(x)
            finally:
                in_flight -= 1

    out = await asyncio.gather(*(run(x) for x in items))
    if stats is not None:
        stats["peak"] = peak
    return list(out)


async def pipeline(source: list, stage_fns: list, queue_size: int, workers_per_stage: int,
                   stats: dict | None = None) -> list:
    """Feed items through async stages fn1 -> fn2 -> ... using bounded queues between stages.

    - One producer task puts source items into queue 0, then one _STOP per worker of stage 0.
    - Stage i has `workers_per_stage` workers reading queue i and writing queue i+1.
    - When a worker reads _STOP, it exits; the LAST worker of stage i to exit sends _STOP for
      every worker of stage i+1 (or, for the last stage, to the collector).
    - If any fn raises, cancel everything and re-raise that exception.
    - stats["peak_q"] = list of the max qsize seen for each queue (checked right after each put).
    Returns outputs of the last stage (any order).
    """
    n = len(stage_fns)
    queues = [asyncio.Queue(maxsize=queue_size) for _ in range(n + 1)]
    peaks = [0] * (n + 1)
    alive = [workers_per_stage] * n
    results: list = []

    async def put(i, x):
        await queues[i].put(x)
        peaks[i] = max(peaks[i], queues[i].qsize())

    async def producer():
        for x in source:
            await put(0, x)
        for _ in range(workers_per_stage):
            await put(0, _STOP)

    async def worker(i):
        fn = stage_fns[i]
        while True:
            x = await queues[i].get()
            if x is _STOP:
                alive[i] -= 1
                if alive[i] == 0:
                    downstream = workers_per_stage if i + 1 < n else 1
                    for _ in range(downstream):
                        await put(i + 1, _STOP)
                return
            await put(i + 1, await fn(x))

    async def collector():
        while True:
            x = await queues[n].get()
            if x is _STOP:
                return
            results.append(x)

    tasks = [asyncio.create_task(producer()), asyncio.create_task(collector())]
    tasks += [asyncio.create_task(worker(i)) for i in range(n) for _ in range(workers_per_stage)]
    try:
        await asyncio.gather(*tasks)
    except BaseException:
        for t in tasks:
            t.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise
    if stats is not None:
        stats["peak_q"] = peaks
    return results


async def gather_settled(coros: list) -> list:
    """Run all; never raise. Return [("ok", value) | ("err", exception)] in input order."""
    out = await asyncio.gather(*coros, return_exceptions=True)
    return [("err", r) if isinstance(r, BaseException) else ("ok", r) for r in out]
