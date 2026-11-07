# W2 D2: circuit breaker

Primer: `knowledge/02-concurrency-and-reliability.md` §3.

## The one idea

When a dependency is down, calling it is worse than useless: you burn threads and latency budget,
and you hammer it while it tries to recover. A circuit breaker **fails fast** after repeated
failures, then **probes carefully** before trusting it again.

```
          failures >= threshold                 reset_timeout elapsed
 CLOSED ───────────────────────────▶ OPEN ───────────────────────────▶ HALF_OPEN
   ▲                                   ▲                                  │
   │        success_threshold          │           any failure            │
   └───────────── successes ───────────┴──────────────────────────────────┘
```

- **CLOSED**: calls pass. Count consecutive failures; a success resets the count.
- **OPEN**: calls are rejected immediately (`CircuitOpen`) until `reset_timeout` has elapsed.
- **HALF_OPEN**: allow at most `half_open_max` **in-flight** trial calls. Any failure reopens (with a
  fresh timer). `success_threshold` successes close it.

The API is split into `allow()` (before the call) and `record_success()` / `record_failure()`
(after), because real calls are concurrent: several can be in flight between allow and record.

## Today's build (`w2d2_breaker.py`)

`CircuitBreaker(failure_threshold, reset_timeout, half_open_max, success_threshold, clock)` with
`state`, `allow() -> bool`, `record_success()`, `record_failure()`, and `call(fn)` that wraps all
three and raises `CircuitOpen` when rejected.

## Staff angle

A breaker turns a slow failure into a fast one: that is only good if the caller has a **fallback**
(cached answer, degraded mode, a smaller model, "try again later"). Staff design reviews ask
"what does the user see when this breaker is open?" If the answer is "a 500", the breaker only
protected the dependency, not the product. Also: one breaker per dependency per instance is the
default; per-endpoint breakers avoid one bad endpoint taking down calls to healthy ones.
