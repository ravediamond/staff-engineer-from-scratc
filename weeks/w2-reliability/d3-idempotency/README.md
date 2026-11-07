# W2 D3: idempotency keys and exactly-once effects

Primer: `knowledge/02-concurrency-and-reliability.md` §4.

## The one idea

Networks give you **at-least-once** delivery: after a timeout you do not know if the server
did the work. The only way to make retries safe for side effects is to make the operation
**idempotent**: doing it twice has the same effect as once. For operations that are not
naturally idempotent (charge a card, send an email, launch a training job), the client sends an
**idempotency key** and the server remembers what it did for that key (Stripe's API is the
reference design).

Server logic, per key:

| Stored state | Same payload fingerprint | Different fingerprint |
|---|---|---|
| none | mark IN_FLIGHT, execute, store result | — |
| IN_FLIGHT | 409 "still processing" (client retries later) | 409 |
| COMPLETED | return the **stored** result, do **not** execute | **422 conflict**: key reused for another request |
| (execution raised) | delete the key so a retry can execute | — |

The fingerprint check is what stops a client bug (reusing a key for a different payment) from
silently returning someone else's result.

**Exactly-once effect = at-least-once delivery + idempotent processing.** Nobody delivers exactly
once; systems that claim it dedupe.

## Today's build (`w2d3_idempotency.py`)

- `fingerprint(payload)`: SHA-256 of canonical JSON (sorted keys, no whitespace).
- `IdempotencyStore(ttl, clock).execute(key, payload, fn)` with the table above, raising
  `InFlight` / `KeyConflict`, and expiring keys after `ttl`.
- `Ledger.transfer(key, src, dst, amount)`: balances change exactly once per key, even under retries.

## Staff angle

The hard part is not the table, it is **atomicity between "store the result" and "do the effect"**.
If the effect is in your DB, write the effect and the idempotency record in the same transaction.
If the effect is external (a payment provider, an email), you need the provider's own idempotency
key, or an outbox. In agent harnesses: every tool with side effects needs an idempotency key
derived from (run id, step id), so a replayed or retried step cannot double-act.
