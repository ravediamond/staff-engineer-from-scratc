"""W2 D5: bounded concurrency, multi-stage pipeline with backpressure, settled gather."""
import asyncio

_STOP = object()


async def bounded_map(fn, items: list, concurrency: int, stats: dict | None = None) -> list:
    """await fn(item) for every item, at most `concurrency` at once. Results in input order.
    If stats is given, set stats["peak"] to the max number of fn calls in flight."""
    # TODO
    raise NotImplementedError


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
    # TODO
    raise NotImplementedError


async def gather_settled(coros: list) -> list:
    """Run all; never raise. Return [("ok", value) | ("err", exception)] in input order."""
    # TODO
    raise NotImplementedError
