# W15 D1: MVCC and isolation levels

> **Full lesson for this day:** [`../README.md`](../README.md#day-1-mvcc-and-isolation-levels) (the week page: concepts from zero, examples, traps).
> This file is the one-page summary with the staff angle. Order of work: `predict.md` → the lesson → `predict_run.py` → the exercise → the review file → `questions.md`.

Primer: `knowledge/19-databases.md` §1.

## The one idea

Postgres (and most modern databases) never overwrite a row: an update writes a **new version** stamped
with the transaction that created it. A reader decides which versions it may see from its **snapshot**:
the set of transactions that had committed when the snapshot was taken. Readers never block writers.

Isolation level = when the snapshot is taken, and what is checked at write/commit:

| Level | Snapshot | Prevents | Still possible |
|---|---|---|---|
| Read committed (Postgres default) | per statement | dirty reads | non-repeatable reads, **lost updates** (read-modify-write), write skew |
| Snapshot / repeatable read | per transaction | the above + lost updates (first committer wins: the second gets a serialization failure and retries) | **write skew** |
| Serializable | per transaction + tracking of what was read | everything: the result equals some serial order | nothing; costs retries |

**Lost update:** two transactions read a counter (10), both write 11. **Write skew:** two doctors are
on call; each checks "is someone else on call?" (yes), each removes themself. Each wrote a different
row, so first-committer-wins sees no conflict; the invariant "at least one on call" is broken.

Old versions that no snapshot can see any more are garbage: **VACUUM** removes them. One long-running
transaction holds back the horizon for the whole database (table bloat).

## Today's build (`w15d1_mvcc.py`)

`MVCCStore`: `begin`, `read`, `write`, `commit`, `abort`, `vacuum`.

## Staff angle

Say the anomaly, not the level name: "this is a read-modify-write, so under read committed two
requests lose an update; I would use an atomic `UPDATE … SET n = n + 1`, or `SELECT … FOR UPDATE`, or
serializable with retries". And know that any level above read committed means your code must retry
on serialization failures.
