# W2 D5: asyncio, bounded concurrency, pipelines, backpressure

Primer: `knowledge/02-concurrency-and-reliability.md` §6.

## The one idea

**Backpressure** = a slow consumer slows down the producer, instead of the queue between them
growing without bound until the process dies of OOM. In asyncio, that is one parameter:
`asyncio.Queue(maxsize=N)`. When full, `await q.put(x)` suspends the producer.

Three tools you need for every LLM/agent workload (where each call is 1–30 s of I/O wait):

| Tool | What it does | Footgun |
|---|---|---|
| `asyncio.Semaphore(n)` | at most n tasks inside the block | forgetting it: 10k concurrent requests → 429 storm |
| `asyncio.Queue(maxsize)` + worker tasks | pipeline stages with backpressure | `maxsize=0` means **unbounded** |
| `asyncio.wait_for(coro, t)` | timeout, cancels the inner task | catching `CancelledError` and swallowing it |

Little's law sizes everything: **in-flight = throughput × latency.** To do 50 req/s against a
model with 4 s latency you need 200 concurrent calls, no more (more just queues server-side).

## Today's build (`w2d5_async.py`)

- `bounded_map(fn, items, concurrency)`: async, results in input order, at most `concurrency` in flight, records the peak in `stats["peak"]`.
- `pipeline(source, stage_fns, queue_size, workers_per_stage)`: multi-stage, bounded queues, sentinel shutdown,
  first exception propagates, output order = completion order (tests sort). Records peak queue sizes.
- `gather_settled(coros)`: like `Promise.allSettled`: list of `("ok", value)` or `("err", exc)`.

## Staff angle

Every batch-eval or embedding-backfill job you will design is this lab at scale. The staff
questions: what is the bottleneck resource (provider rate limit, GPU, DB writes)? Size concurrency
from Little's law against that resource, not "as many as possible". How do you resume after a crash
halfway through 10M items (checkpoint offsets, idempotent writes)? What happens to items that
fail 3 times (dead-letter, not infinite retry)?
