# Questions

1. Why jitter? Why "full" jitter rather than ±10%?
2. Deadline vs max attempts: why do production RPC systems prefer deadlines?
3. What is retry amplification? Give the number for 4 layers × 3 retries each, and two mitigations.
4. An LLM API returns 429 with a `Retry-After: 20` header. What does your client do?
5. In an agent harness, a tool call times out after it may have charged a customer. Retry or not?

## Model answers

1. Synchronized clients retry in waves that recreate the overload. Jitter decorrelates them. Full jitter (uniform over the whole [0, backoff]) gives the lowest total work and fastest completion in AWS's simulations; small jitter keeps clients clustered.
2. The user cares about total latency, not attempt count. A deadline bounds end-to-end time whatever each attempt costs, and propagating it lets downstream services drop work nobody will read. Max attempts with slow attempts can blow far past any SLO.
3. Each layer multiplies: 4 attempts per layer at 4 layers = 4⁴ = 256 backend calls per user request when the backend is down, which turns a partial outage into a total one. Mitigations: retry at one layer only, retry budgets (≤10% extra traffic), circuit breakers, and propagating "do not retry" signals upstream (e.g. gRPC pushback).
4. Respect it: wait at least 20 s (with jitter on top), or fail fast to the caller if 20 s exceeds the deadline. Count it against the retry budget. Treat 429 as a capacity signal: lower client-side concurrency (an AIMD-style limiter) instead of only waiting.
5. Not blindly: the outcome is unknown, not failed. Retry only if the tool call carries an idempotency key the server deduplicates on (W2 D3). Otherwise first query the side-effect state ("did charge X happen?"), or surface it to a human. Never let the model re-issue a non-idempotent action because it "didn't see a response".
