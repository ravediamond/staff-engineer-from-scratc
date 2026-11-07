# W3 D5: leases and fencing tokens

Primer: `knowledge/03-distributed-systems.md` §5. Reference: Martin Kleppmann, "How to do distributed locking" (2016).

## The one idea

A distributed lock is really a **lease**: you hold it until time T unless you renew. The
problem: the holder cannot know reliably that its lease is still valid. A GC pause, a VM stall
or a network delay can last longer than the lease. The client wakes up, believes it still holds
the lock, and writes, while a second client legitimately holds it too.

```
client A:  acquire(token=33) ── [GC pause 40 s ...........] ── write(token=33) ✗ must be rejected
lock svc:            lease A expires ── client B acquire(token=34) ── write(token=34) ✓
storage:                                                   max_token=34 → rejects 33
```

**Fencing token:** the lock service hands out a strictly increasing number with every grant.
The **storage** remembers the highest token it has accepted per resource and rejects anything
lower. Safety moves from "the client checks the time" (impossible to make safe) to "the resource
checks a number" (easy).

## Today's build (`w3d5_fencing.py`)

- `LockService(lease, clock)`: `acquire(client) -> token | None`, `renew(client, token) -> bool`, `release(client, token)`.
  Tokens increase on every grant, including re-acquire after expiry.
- `FencedStorage`: `write(resource, value, token)` accepts only `token >= max_token[resource]`; raises `StaleToken` otherwise.
- `simulate_gc_pause()` returns the final storage value and the list of accepted writers for the scenario in the diagram.

## Staff angle

Two questions to ask in any design that has a "leader" or "exclusive worker": (1) what is the
fencing mechanism at the resource? (2) what happens if the old leader keeps running? For
training jobs: a preempted-then-revived trainer writing checkpoints to the same path as its
replacement corrupts the run unless checkpoint writes are fenced (run generation number in the
path or a conditional write). For agent workers pulling jobs from a queue: visibility-timeout
expiry plus a slow worker equals two workers on one job, so job side effects need idempotency (W2 D3).
