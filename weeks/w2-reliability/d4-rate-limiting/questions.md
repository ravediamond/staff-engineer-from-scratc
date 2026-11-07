# Questions

1. Token bucket vs leaky bucket vs sliding window: one sentence each, and when you pick each.
2. Why compute refills lazily instead of a timer per key?
3. Design rate limiting for an LLM API gateway: 50k customers, limits in requests AND tokens per minute, 20 gateway instances.
4. Your limiter uses Redis. Redis is down. Fail open or fail closed? Defend it.
5. Why is limiting on requests the wrong unit for LLM traffic, and how do you charge tokens you do not know yet?

## Model answers

1. Token bucket: average rate with bounded bursts, the default for APIs. Leaky bucket: smooths output to a constant rate (shaping), good for protecting a fragile downstream. Sliding window log: exact, memory heavy, for small limits or audits. Sliding window counter: approximate, O(1) memory, good default at scale.
2. A million keys means a million timers. Lazy refill computes the same tokens from elapsed time in O(1) on access, with zero work for idle keys.
3. Admission at each gateway: a local token bucket per (customer, dimension), refilled from a quota leased from a central allocator (Redis or a dedicated service) every ~1 s in proportion to local demand. Token dimension: charge estimated input + max_tokens at admission, refund the difference after completion. Global exactness is traded for no per-request hop; hot customers get sticky routing. Return 429 with Retry-After and expose remaining quota in headers.
4. Usually fail open with a local fallback limit (per-instance limit/N): the limiter protects capacity, and a Redis blip should not become a total outage. Fail closed when the limit guards money or abuse (free-tier fraud, expensive GPU endpoints). It is a business decision, so write it in the design doc.
5. Request cost varies about 1000× (50 tokens vs 200k context), so requests do not track load. Reserve estimated tokens at admission (input counted exactly, output = max_tokens or a predicted p95), then reconcile with actual usage when the response completes, crediting or debiting the bucket.
