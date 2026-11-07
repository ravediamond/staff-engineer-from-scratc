# Week 2: reliability primitives (harness foundations)

Every agent harness, RAG service and training job you will design is a pile of remote calls
that fail. This week builds the five primitives that turn "it works on my machine" into "it
works at 3am under partial failure": retries with deadlines, circuit breakers, idempotency,
rate limiting, backpressure. Each comes with an injected clock, because untestable time is the
#1 source of flaky reliability code.

Primer: `knowledge/02-concurrency-and-reliability.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | retries, full jitter, deadlines, retry budget | retries non-retryable errors |
| d2 | circuit breaker (closed / open / half-open) | half-open admits unlimited trial calls |
| d3 | idempotency keys and exactly-once effects | cached result returned for a different payload |
| d4 | token bucket, sliding window log and counter | refill not capped at capacity |
| d5 | asyncio: bounded concurrency, pipelines, backpressure | unbounded queue |
