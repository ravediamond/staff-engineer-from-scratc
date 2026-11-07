# 02. Concurrency and reliability

## §1 Retries

Retry only transient failures (429, 5xx except 501, timeouts, resets). Exponential backoff with **full
jitter**: `uniform(0, min(cap, base·2^n))`. Respect `Retry-After`. Non-idempotent operations require
idempotency keys.

## §2 Deadlines and budgets

Deadlines (absolute time) propagate downstream; each hop gets the remaining time. Retry budgets cap
retries at a fraction (~10%) of traffic. Retry at exactly one layer: N layers × r retries = rᴺ amplification.

## §3 Circuit breakers

Closed → open after failures → half-open after a timeout with a limited number of trial calls → closed
after successes, or open again on any failure. Needs a fallback to protect the user, not just the dependency.

## §4 Idempotency

Key + payload fingerprint; table: absent → execute; in-flight → 409; completed, same payload → replay
the stored response; different payload → 422; failure → release the key. Exactly-once **effect** =
at-least-once delivery + idempotent processing. Store the record atomically with the effect.

## §5 Rate limiting

Token bucket (bursty, standard), sliding window log (exact, memory heavy), sliding window counter
(approximate, O(1)). For LLM traffic: limit tokens, not requests; reserve at admission, reconcile after.
Fleet-wide: local buckets refilled from a central allocator.

## §6 Concurrency in Python, and backpressure

| Workload | Tool |
|---|---|
| many I/O waits (APIs, LLM calls) | asyncio (or threads) |
| CPU-bound pure Python | processes (`multiprocessing`, `ProcessPoolExecutor`) |
| CPU-bound in C extensions that release the GIL (numpy, tokenizers) | threads can work |

Little's law: `L = λ·W`. Bounded queues (`maxsize`) give backpressure; unbounded queues hide overload
until OOM. Never swallow `CancelledError`.

## Failure vocabulary for design rounds

Timeouts, retries with jitter, circuit breakers, bulkheads (separate pools per dependency), load
shedding (reject early with 503 to protect latency for admitted requests), graceful degradation,
hedged requests (send a second request after the p95 delay to cut tail latency, with a budget).

## Questions

1. Hedged requests: what are they, when do they help, what do they cost?
<details><summary>Answer</summary>After waiting about the p95 latency, send a duplicate request to another replica and take the first response (Dean & Barroso, "The Tail at Scale"). It cuts tail latency a lot for a few percent extra load. Only for idempotent reads; cap it with a budget and cancel the loser.</details>

2. Bulkheads: explain with an example from an agent harness.
<details><summary>Answer</summary>Separate concurrency pools per tool or dependency (e.g. 20 slots for web search, 5 for the code sandbox), so a slow or failing tool cannot exhaust the threads or connections that other tools and the model calls need. It is the ship-compartment analogy.</details>

3. A downstream returns 503 for 10 minutes. Describe what each layer of a well-designed caller does during and after.
<details><summary>Answer</summary>The executor retries with jitter within the deadline and retry budget; the breaker opens after the threshold, so calls fail fast and the fallback (cache, degraded answer, queue for later) serves users; load shedding protects upstream latency; half-open probes test recovery; on success the breaker closes gradually; queued work drains at a rate-limited pace to avoid a second spike. Alerts fire on breaker state and error budget burn.</details>

4. Why can't you get exactly-once delivery, and what do you build instead?
<details><summary>Answer</summary>The sender cannot distinguish a lost message from a lost acknowledgement, so it must resend and duplicates are possible. Build at-least-once delivery plus idempotent consumers: dedupe by message id stored atomically with the effect, or transactional processing that commits output and offsets together.</details>
