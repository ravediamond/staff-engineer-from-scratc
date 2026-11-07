# Questions

1. Define backpressure. Name three ways a system can apply it.
2. Little's law: state it, then use it to size a batch eval job against an API with 6 s p50 latency and 600 RPM limit.
3. Threads vs asyncio vs processes in Python for (a) 10k LLM API calls, (b) tokenizing 10 GB of text, (c) a mix.
4. Your 50M-document embedding backfill crashes at 60%. What should the design have included?
5. What goes wrong if you catch `asyncio.CancelledError` and do not re-raise it?

## Model answers

1. A slow consumer pushes back on the producer instead of buffering without limit. Ways: blocking bounded queues, credit or flow-control windows (TCP, HTTP/2, gRPC), load shedding with 429/503 so clients back off, and pull-based consumption (Kafka consumers pull at their own pace).
2. L = λW. 600 RPM = 10 req/s; 10 req/s × 6 s = 60 in flight. Above 60 you only queue at the provider and trip 429s. Set the semaphore around 60, maybe 70 to absorb latency variance, and pair it with a token-bucket limiter at 10/s.
3. (a) asyncio (or threads): I/O-bound, the GIL is irrelevant, asyncio scales to thousands of in-flight calls cheaply. (b) processes (multiprocessing, or a Rust-backed tokenizer that releases the GIL): CPU-bound. (c) asyncio for I/O, CPU work offloaded via `run_in_executor` to a process pool. (Free-threaded Python 3.13+ changes (b) over time.)
4. Checkpointed progress (persisted offsets or a done-set), idempotent writes keyed by doc id + model version so a restart re-runs safely, bounded queues, per-item retry with a dead-letter queue, a rate limiter, metrics (throughput, error rate, ETA), and a small canary run before the full one.
5. Cancellation stops propagating: `wait_for` timeouts, task-group shutdown and Ctrl-C hang or leak tasks, because the task keeps running after its owner asked it to stop. Rule: clean up in `finally`, and re-raise `CancelledError` if you catch it.
