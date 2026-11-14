# W15 D4: replication, as the application sees it

Primer: `knowledge/19-databases.md` §4. Builds on W3 (quorums, Raft): here it is single-leader replication, the default of Postgres and MySQL.

## The one idea

One **primary** takes writes and ships its log to **replicas**. Each write has a position in the log
(**LSN**). A replica has applied the log up to some LSN: the difference is **replication lag**.

- **Asynchronous** (default): the primary acknowledges before replicas have the write. Fast; a failover
  loses the unreplicated tail (RPO > 0), and reads on replicas are stale.
- **Synchronous**: the primary waits for at least one replica. No loss on failover of one node; every
  write pays the round trip, and with a single sync replica its failure blocks writes (use "any 1 of 2").

Reading from replicas scales reads and creates three user-visible anomalies:

| Anomaly | Example | Fix |
|---|---|---|
| no **read-your-writes** | you post a comment, reload, it is gone | route the session's reads to a replica at or past the LSN of its last write, else to the primary |
| non-**monotonic reads** | reload twice: comment appears, disappears | remember the highest LSN the session has seen; never read from a replica behind it |
| stale decision | check stock on a replica, then write | decisions that guard writes read from the primary, in the write's transaction |

**Failover**: promote the most advanced replica; the old primary must be **fenced** (W3 D5) or you get
split brain; writes it acknowledged but had not shipped are gone, or worse, come back as conflicts.

## Today's build (`w15d4_replication.py`)

`Cluster`: `write`, `replicate`, `read` (session-aware routing), `failover`.

## Staff angle

Put numbers on it in a design: "async replication, lag p99 under 1 s, read-your-writes through an LSN
token in the session, RPO equal to the lag at failure, RTO about a minute with automated promotion".
And know when not to read from replicas at all: money, permissions, anything that guards a write.
