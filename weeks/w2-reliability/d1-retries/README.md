# W2 D1: retries, jitter, deadlines, retry budgets

Primer: `knowledge/02-concurrency-and-reliability.md` §1–2.

## The one idea

A retry is a bet that the failure was transient. Four rules make the bet safe:

1. **Only retry what can succeed on retry.** 429, 500, 502, 503, 504, timeouts, connection resets:
   yes. 400, 401, 403, 404, 409, 422: no, the second call fails the same way and you just doubled
   the load. Non-idempotent operations: only with an idempotency key (W2 D3).
2. **Exponential backoff with full jitter.** `sleep = uniform(0, min(cap, base · 2^attempt))`.
   Without jitter, 10,000 clients that failed together retry together and knock the service
   over again (thundering herd). Full jitter spreads them (AWS Architecture Blog, "Exponential
   Backoff and Jitter").
3. **Deadlines, not attempt counts.** The caller has a total budget (say 2 s). Each attempt gets
   `remaining = deadline - now`, and you stop when the next sleep would cross the deadline.
   Pass the remaining budget downstream (gRPC deadline propagation), so a callee does not keep
   working on a request whose caller already gave up.
4. **Retry budgets.** Each layer retrying 3 times turns 1 request into 3⁵ = 243 at depth 5.
   A budget caps retries at a fraction of normal traffic (e.g. 10%): when the backend is truly
   down, you stop amplifying (Google SRE book, ch. 22 "Addressing Cascading Failures").

## Today's build (`w2d1_retry.py`)

- `is_retryable_status(code)`.
- `backoff_delay(attempt, base, cap, rng)`: full jitter.
- `call_with_retry(fn, ...)`: calls `fn(remaining_seconds)`, retries retryable errors, respects a deadline,
  uses injected `clock`, `sleep`, `rng`. Raises the last error, or `DeadlineExceeded` if there is no time for another attempt.
- `RetryBudget(ratio, min_per_window)`: `record_request()`, `try_spend()` → bool.

## Staff angle

The staff question is "where should retries live?" Answer: **at exactly one layer**, usually the
one closest to the user that knows the deadline, with every other layer failing fast. In an
agent harness that means the tool-call executor owns retries; the model loop does not also
retry the whole step. Write it down in the design doc, because the default is that every team
adds its own.
