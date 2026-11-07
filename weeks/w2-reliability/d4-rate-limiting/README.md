# W2 D4: rate limiting

Primer: `knowledge/02-concurrency-and-reliability.md` §5.

## The one idea

Three algorithms, three trade-offs:

| Algorithm | State per key | Burst behaviour | Accuracy |
|---|---|---|---|
| **Token bucket** (rate r, capacity b) | 2 numbers (tokens, last refill time) | allows bursts up to b, then r/s | exact for its model |
| **Sliding window log** | every timestamp in the window | none beyond limit | exact, memory O(limit) |
| **Sliding window counter** | 2 counters (current, previous window) | smoothed | approximate (assumes uniform previous window) |

Token bucket refill, computed lazily on each call (no background timer):
`tokens = min(capacity, tokens + (now - last) · rate)`. The `min` is the invariant
**`0 <= tokens <= capacity`**. Forget it and an idle client accumulates unlimited burst credit.

Sliding window counter estimate at time `now` in window starting `w0`:
`count ≈ prev_count · (1 - (now - w0)/W) + curr_count`. Cloudflare reported 0.003% wrong decisions
with this on real traffic.

## Today's build (`w2d4_ratelimit.py`)

`TokenBucket(rate, capacity, clock).allow(cost=1)`, `SlidingWindowLog(limit, window, clock).allow()`,
`SlidingWindowCounter(limit, window, clock).allow()`, and `KeyedLimiter(factory).allow(key)`.

## Staff angle

For LLM APIs, limit on **tokens, not requests**: one request can be 50 tokens or 200k. Providers
do both (RPM and TPM). Charge the bucket with the estimated cost at admission, then reconcile with
the real cost after the response. In a fleet, a per-instance limiter of `limit/N` drifts when
traffic is uneven; a central limiter (Redis + Lua script, atomic) is exact but adds a hop.
The common staff answer: local token buckets with periodic quota sync from a central allocator.
