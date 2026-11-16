# Week 2: Reliability and concurrency

**Everything you need for this week is on this page.** You need week 1 (invariants, injected clocks). Nothing from other folders is required.

Every system you will design calls other systems over a network, and networks fail. Staff design rounds are decided in the deep dives, and the deep dives are these five topics: what happens on a timeout, when a dependency is down, when a request is sent twice, when a client sends too much, when a consumer is slower than its producer. This week you build each mechanism small enough to test exactly.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [What can go wrong on a network call](#what-can-go-wrong-on-a-network-call).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-retries-jitter-deadlines-retry-budgets), [Day 2](#day-2-circuit-breaker), [Day 3](#day-3-idempotency-keys), [Day 4](#day-4-rate-limiting), [Day 5](#day-5-asyncio-bounded-concurrency-backpressure).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w2dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w2dN_*.py` | tests | run, never edit |
| `review_w2dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w2-reliability/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w2-reliability/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w2-reliability/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w2-reliability/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The failure | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-retries` | a call fails for a moment | retries with backoff, jitter, a deadline, a retry budget | which errors get retried |
| Tue | `d2-circuit-breaker` | a dependency is down for minutes | a three-state circuit breaker | how many trial calls are let through |
| Wed | `d3-idempotency` | a request arrives twice | idempotency keys; a ledger that moves money exactly once | what is checked besides the key |
| Thu | `d4-rate-limiting` | a client sends too much | token bucket, two sliding windows, a per-key limiter | a missing bound |
| Fri | `d5-backpressure` | a consumer is slower than its producer | bounded concurrency and a bounded pipeline in asyncio | a queue with no limit |

## What can go wrong on a network call

You call a service and wait. Four outcomes:

| Outcome | What you know |
|---|---|
| success | the work was done |
| an error that says "your request is wrong" (HTTP 400, 404, 422) | sending it again fails the same way |
| an error that says "I cannot right now" (HTTP 429, 500, 503) | sending it again later may work: a **transient** failure |
| **no answer before your timeout** | **nothing.** The request may be lost, still running, or done with the reply lost |

The last line is the root of the week. After a timeout you cannot tell "not done" from "done, answer lost". Everything below is a way to stay correct anyway.

Three words used all week:

- **Idempotent**: doing the operation twice has the same effect as doing it once. "Set the balance to 100" is; "add 100 to the balance" is not.
- **Latency percentiles**: p50 is the latency that half of the requests beat; p99 is the one that 99% beat. Users feel the p99.
- **Cascading failure**: one overloaded service makes its callers slow, their callers pile up, and the outage spreads upward.

HTTP status codes in one line: 2xx success; 4xx the caller's fault; 5xx the server's fault; 429 "too many requests".

## Day 1: Retries, jitter, deadlines, retry budgets

Folder: `d1-retries`. Exercise: `w2d1_retry.py`.

### A retry is a bet

A retry bets that the failure was transient. A badly made bet turns a small failure into an outage, because retries are extra load on a service that is already struggling. Four rules make the bet safe.

### Rule 1: only retry what can succeed

Retry: 429, 500, 502, 503, 504, timeouts, connection resets. Do not retry: 400, 401, 403, 404, 409, 422. The second call fails the same way and you have doubled the load. Retrying everything is today's review bug. An operation that is not idempotent may be retried only with an idempotency key (Wednesday).

### Rule 2: exponential backoff with full jitter

Wait before retrying, and wait longer each time: `base · 2^attempt`, up to a cap. That is **exponential backoff**.

Backoff alone is not enough. Ten thousand clients that failed at the same instant all wait exactly 1 s, retry together, fail together, wait exactly 2 s, and hit the service again as one wall of requests: a **thundering herd**. **Jitter** adds randomness so they spread out. **Full jitter** draws the wait uniformly between 0 and the backoff value:

```
sleep = uniform( 0, min(cap, base · 2^attempt) )            attempt = 0, 1, 2, …
```

```python
import random
rng = random.Random(0)                       # seeded: reproducible
[round(rng.uniform(0, min(10.0, 0.5 * 2 ** a)), 2) for a in range(5)]     # five waits, each inside a growing range
```

The random generator is passed in, like the clock.

### Rule 3: a deadline, not a number of attempts

The caller has a total time budget, say 2 seconds. That is the **deadline**. "Three attempts" says nothing about time: three attempts of 5 seconds each answer long after anyone is listening.

Each attempt is given what remains, `deadline − now`. Before sleeping, check that the sleep still fits before the deadline; if not, stop now. The remaining time is also passed **downstream** to the service you call, so that it does not keep working for a caller that has already given up (gRPC does this for you; it is called deadline propagation).

### Rule 4: a retry budget

Retries multiply across layers. If each of 5 layers retries 3 times, one user request can become `3⁵ = 243` requests at the bottom. A **retry budget** caps retries at a fraction of normal traffic, for example 10%: count the requests seen in a recent window; a retry is allowed only while the number of retries in that window stays under `ratio × requests`, plus a small fixed minimum so that a client with almost no traffic can still retry. When the backend is truly down, the budget runs out and the client stops making things worse.

A sliding window over time is a queue of timestamps: append on each event, drop from the front what is older than the window.

### Traps of the day

- Backoff with no jitter, or jitter added on top of a fixed wait.
- Retrying a 400.
- Sleeping past the deadline.
- `2^attempt` with attempts counted from 1 where the formula counts from 0.
- A budget that counts retries as requests: retries then pay for more retries.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `is_retryable_status` | which status codes are worth a retry | rule 1 |
| `backoff_delay` | full jitter | rule 2 |
| `call_with_retry` | call `fn(remaining_seconds)`; retry only retryable errors; respect the deadline; injected `clock`, `sleep`, `rng` | rules 1–3 |
| `RetryBudget` | `record_request`, `try_spend` | rule 4 |

Run: `uv run pytest weeks/w2-reliability/d1-retries -k "not review"`

---

## Day 2: Circuit breaker

Folder: `d2-circuit-breaker`. Exercise: `w2d2_breaker.py`.

### The idea

Retries handle a failure that lasts milliseconds. When a dependency is down for minutes, calling it is worse than useless: each call holds a thread and a connection until it times out, your own latency explodes, and you keep hitting a service that is trying to recover.

A **circuit breaker** sits in front of the dependency. After repeated failures it **fails fast**: calls are refused at once, without touching the network. After a pause it lets a few trial calls through to see whether the dependency is back.

### Three states

```
          failures ≥ threshold                  reset_timeout elapsed
 CLOSED ───────────────────────────▶ OPEN ───────────────────────────▶ HALF_OPEN
   ▲                                   ▲                                  │
   │     enough trial successes        │          any trial failure       │
   └───────────────────────────────────┴──────────────────────────────────┘
```

| State | Calls | Leaves when |
|---|---|---|
| **CLOSED** (normal) | pass | consecutive failures reach the threshold → OPEN. A success resets the count. |
| **OPEN** | refused immediately | `reset_timeout` has elapsed → HALF_OPEN |
| **HALF_OPEN** | at most `half_open_max` trial calls in flight; the rest refused | enough successes → CLOSED; **any** failure → OPEN, with a **fresh** timer |

The names come from electricity: a closed circuit lets current through.

### Two details that make it correct

**The move from OPEN to HALF_OPEN is lazy.** There is no background timer. When someone asks `allow()` or reads the state, the breaker compares the clock with the moment it opened.

**Before and after are separate calls.** `allow()` is asked before the call; `record_success()` or `record_failure()` is told after. Real calls overlap in time: several can be in flight between an `allow` and its `record`. That is why HALF_OPEN counts **in-flight** trials: each allowed trial takes a slot, and its result gives the slot back.

The limit on trial calls is the point of HALF_OPEN: without it, the first moment after the pause sends full traffic to a service that is barely back, and knocks it over again. That is today's review bug.

A failed trial must reopen the breaker and restart the timer. If the timer is not restarted, the breaker flips straight back to HALF_OPEN and the dependency is hit again at once.

### Traps of the day

- A success in CLOSED that does not reset the failure count: unrelated failures spread over a day open the breaker.
- A reopened breaker with the old timer.
- Unlimited trial calls in HALF_OPEN: the recovering service gets full traffic.
- Slots never given back after a trial.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `CircuitBreaker.state` | the current state, with the lazy OPEN → HALF_OPEN move | two details |
| `allow` | may this call go? | three states |
| `record_success`, `record_failure` | the transitions | three states |
| `call` | wraps the three; raises `CircuitOpen` when refused | — |

Run: `uv run pytest weeks/w2-reliability/d2-circuit-breaker -k "not review"`

---

## Day 3: Idempotency keys

Folder: `d3-idempotency`. Exercise: `w2d3_idempotency.py`.

### The problem

A client asks the server to charge a card. The request times out. Was the card charged? The client cannot know (see the table at the top). Not retrying may lose a payment. Retrying may charge twice.

Networks give **at-least-once** delivery: a message that matters is resent until acknowledged, so it can arrive more than once. The only way to make that safe for side effects is to make the operation **idempotent**.

### The idempotency key

For operations that are not naturally idempotent (charge a card, send an email, launch a training job), the **client** generates a unique key for the operation and sends it with every attempt. The **server** remembers what it did for each key. Stripe's API is the reference design.

Per key, the server stores a state and a **fingerprint** of the request payload:

| Stored state | Same fingerprint | Different fingerprint |
|---|---|---|
| nothing | mark IN_FLIGHT, execute, store the result as COMPLETED | — |
| IN_FLIGHT | refuse: "still processing" (the client retries later) | refuse |
| COMPLETED | return the **stored** result; do **not** execute again | refuse: the key was reused for another request |
| the execution raised | forget the key, so a retry can execute | — |

- **IN_FLIGHT** covers two copies of the request arriving at the same moment: the second must not start a second execution.
- **The fingerprint** covers a client bug: the same key sent with a different payload. Without the check, the server would answer a new payment with the stored result of an old one.
- **On failure the key is forgotten.** Nothing was done, so the retry must be allowed to do it.
- Keys expire after a time to live, or the store grows forever.

### A fingerprint

A hash of the payload in a **canonical** form: one text for one content, whatever the order of the keys or the spacing.

```python
import hashlib, json
payload = {"to": "bob", "amount": 10}
canon = json.dumps(payload, sort_keys=True, separators=(",", ":"))     # '{"amount":10,"to":"bob"}'
hashlib.sha256(canon.encode()).hexdigest()[:12]
```

### "Exactly once"

No network delivers a message exactly once. Systems that promise it deliver at least once and **deduplicate**:

```
exactly-once effect = at-least-once delivery + idempotent processing
```

That sentence is worth saying in any design that involves payments, emails or jobs.

### Traps of the day

- The key checked without the fingerprint.
- A second execution started while the first is in flight.
- The key kept after a failed execution: the operation can never be done.
- The result recomputed instead of the stored one returned: for a transfer, the money moves twice.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `fingerprint` | SHA-256 of the canonical JSON | a fingerprint |
| `IdempotencyStore.execute` | the table above; raises `InFlight` or `KeyConflict`; keys expire | the idempotency key |
| `Ledger.transfer` | balances change exactly once per key, under any number of retries | "exactly once" |

Run: `uv run pytest weeks/w2-reliability/d3-idempotency -k "not review"`

---

## Day 4: Rate limiting

Folder: `d4-rate-limiting`. Exercise: `w2d4_ratelimit.py`.

### Why

A service can do a finite amount of work. A **rate limiter** refuses requests beyond a limit, per client, so that one client (or one bug in a loop) cannot take the service down for everyone. Three algorithms, three trade-offs.

### Token bucket

A bucket holds up to `capacity` tokens and gains `rate` tokens per second. A request takes one token (or `cost` tokens); if there are not enough, it is refused.

It allows a **burst** of up to `capacity` requests at once, then a steady `rate` per second. Two numbers per client.

There is no timer adding tokens. The bucket is refilled **lazily**, each time it is asked:

```
tokens = min( capacity, tokens + (now − last) · rate ) ;  last = now
```

**Invariant: `0 ≤ tokens ≤ capacity`.** The `min` is what keeps it. Without it, a client that stays silent for an hour comes back with an hour's worth of tokens and an unlimited burst.

### Sliding window log

Keep the timestamp of every accepted request. To decide: drop the timestamps older than the window, count what is left, accept if the count is below the limit.

Exact: never more than `limit` requests in any window. The cost is memory: one timestamp per request, up to `limit` per client.

### Sliding window counter

Count requests per fixed window (windows aligned on multiples of the window length) and keep only two counters: the current window and the previous one. Estimate the count over the last `W` seconds by assuming the previous window's requests were spread evenly:

```
elapsed  = fraction of the current window already gone       (0 to 1)
estimate = previous · (1 − elapsed) + current
```

Two numbers per client and an approximate answer. Cloudflare measured about 0.003% wrong decisions with it on real traffic.

| Algorithm | State per client | Bursts | Accuracy |
|---|---|---|---|
| token bucket | 2 numbers | up to `capacity` | exact for its model |
| sliding window log | every timestamp in the window | none beyond the limit | exact |
| sliding window counter | 2 counters | smoothed | approximate |

### One limiter per client

A dict from client key to a limiter, created the first time the key is seen, by a **factory** (a function that returns a new limiter).

### Traps of the day

- No `min` in the refill.
- `last` not updated when a request is refused: the same elapsed time is credited twice.
- A window boundary handled with the wrong `<` or `<=`: the docstring gives the convention.
- A refused request recorded in the log or the counter.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `TokenBucket` | lazy refill, `allow(cost)` | token bucket |
| `SlidingWindowLog` | exact | sliding window log |
| `SlidingWindowCounter` | two counters and the estimate | sliding window counter |
| `KeyedLimiter` | one limiter per key, from a factory | one limiter per client |

Run: `uv run pytest weeks/w2-reliability/d4-rate-limiting -k "not review"`

---

## Day 5: asyncio, bounded concurrency, backpressure

Folder: `d5-backpressure`. Exercise: `w2d5_async.py`.

### asyncio in ten lines

Most of the time, a program that calls a model or a database is **waiting**. `asyncio` lets one thread run thousands of waits at once.

- `async def` defines a **coroutine**: a function that can pause.
- `await x` pauses the coroutine until `x` is ready, and lets others run meanwhile.
- A **task** is a coroutine scheduled to run concurrently: `asyncio.create_task(coro)`.
- `asyncio.run(main())` starts everything.

```python
import asyncio

async def work(i):
    await asyncio.sleep(0.01)        # stands for a network call
    return i * 2

async def main():
    return await asyncio.gather(*(work(i) for i in range(5)))     # all five wait at the same time

asyncio.run(main())                  # [0, 2, 4, 6, 8], in about 0.01 s, not 0.05 s
```

Only one coroutine runs at any instant; they take turns at each `await`. So code between two `await`s is never interrupted.

### Bounded concurrency

Start 10 000 calls at once against a model API and you get a storm of 429s. A **semaphore** is a counter of free slots: `async with sem:` waits for a slot, takes it, and gives it back on the way out.

```python
async def limited():
    sem = asyncio.Semaphore(2)
    async def one(i):
        async with sem:              # at most 2 inside at any time
            return await work(i)
    return await asyncio.gather(*(one(i) for i in range(6)))

asyncio.run(limited())
```

`asyncio.gather` returns results in the order of its arguments, whatever the order of completion.

**How much concurrency?** Little's law: **in flight = throughput × latency.** To do 50 requests per second against a model that takes 4 seconds, you need 200 calls in flight. More than that only moves the queue to the server.

### Backpressure

A producer feeds a queue; a consumer empties it. If the producer is faster, the queue grows until the process runs out of memory. **Backpressure** means the slow consumer slows the producer down. In asyncio it is one parameter:

```python
q = asyncio.Queue(maxsize=100)       # when full, `await q.put(x)` pauses the producer
```

`maxsize=0` means **unbounded**: no backpressure at all. It is the default, and today's review bug.

### A pipeline with stages

Each stage is a set of worker tasks that read from an input queue, apply a function, and write to the next queue. Every queue is bounded, so a slow stage slows the stages before it, back to the source.

**Shutting down.** Workers loop forever on `await q.get()`. To stop them, the stage before sends a special object, a **sentinel**, once the real items are done: one per worker of the next stage. A worker that reads the sentinel stops. When all workers of a stage have stopped, that stage sends sentinels to the next one.

**Errors.** If one item fails, the first exception must reach the caller and nothing must hang: remaining tasks are cancelled. A task that is cancelled raises `asyncio.CancelledError` at its current `await`. Never catch it and continue: the task then cannot be stopped.

### Waiting for all, keeping every outcome

`asyncio.gather(*coros, return_exceptions=True)` returns each result **or** the exception object, instead of raising at the first failure. From that you can build "settled" results: `("ok", value)` or `("err", exception)` for each, in order.

`asyncio.wait_for(coro, timeout)` cancels `coro` if it takes too long.

### Traps of the day

- An unbounded queue.
- No semaphore.
- Fewer sentinels than workers: some workers wait forever.
- `CancelledError` swallowed.
- A peak measured after the work, not during: update the counter inside the bounded section.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `bounded_map` | results in input order, at most `concurrency` in flight, the peak recorded | bounded concurrency |
| `pipeline` | stages, bounded queues, sentinel shutdown, first exception propagates | a pipeline with stages |
| `gather_settled` | one `("ok", value)` or `("err", exc)` per coroutine | waiting for all |

Run: `uv run pytest weeks/w2-reliability/d5-backpressure -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w02`, timer on, AI fully off: `uv run pytest drills/w02 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 2 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 2 when you can do these without notes:

- [ ] say what you know after a timeout, and why that is the core problem
- [ ] write full-jitter backoff and explain the thundering herd
- [ ] explain deadlines against attempt counts, and what a retry budget prevents
- [ ] draw the three states of a circuit breaker with every transition
- [ ] explain an idempotency key, the fingerprint check, and "exactly-once effect"
- [ ] compare token bucket, sliding log and sliding counter on memory, bursts and accuracy
- [ ] explain backpressure and size a concurrency limit with Little's law

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/02-concurrency-and-reliability.md`
- Previous week: [`../w1-coding-base/README.md`](../w1-coding-base/README.md) · Next: [`../w3-distributed/README.md`](../w3-distributed/README.md)
