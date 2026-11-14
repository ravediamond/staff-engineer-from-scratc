# W13 D2: replication, ISR, high watermark, acks

Primer: `knowledge/16-streaming-and-messaging.md` §2.

## The one idea

Each partition has one **leader** and followers. Followers **pull** from the leader. Four terms carry
the whole durability story:

| Term | Meaning |
|---|---|
| **LEO** (log end offset) | next offset a replica will write: its log length |
| **ISR** (in-sync replicas) | replicas caught up with the leader recently (`replica.lag.time.max.ms`); the leader is always in it |
| **HW** (high watermark) | `min(LEO of every ISR member)`: everything below it is on all in-sync replicas = **committed** |
| **acks** | what the producer waits for: `0` nothing, `1` leader wrote it, `all` it is below the HW |

Rules that follow:

- **Consumers only see records below the HW.** Otherwise they could read a record that a failover erases.
- `acks=all` + `min.insync.replicas=2` on 3 replicas: an acknowledged write survives one broker loss.
  If the ISR shrinks below `min.insync.replicas`, `acks=all` produces fail (`NotEnoughReplicas`):
  the partition chooses consistency over availability for writes.
- A new leader is elected **from the ISR**. Electing a replica outside the ISR (**unclean** leader
  election) keeps the partition available and silently loses committed data: off by default.
- After a failover, a replica that has records the new leader lacks **truncates** them (leader epochs
  decide where). With `acks=1` those were acknowledged records: that is the data-loss window.

## Today's build (`w13d2_replication.py`)

`Partition(n_replicas, min_insync, unclean)`: `produce`, `acked`, `replicate`, `shrink_isr`, `fetch`,
`fail`, `recover`.

## Staff angle

This is the same problem as your W3 quorum and Raft labs with a different trade: Raft needs a majority
(2f+1 replicas for f failures); ISR replication needs only f+1 because the ISR membership itself is
stored in a consensus system (the KRaft controller quorum, ZooKeeper before Kafka 4.0). In a design
review, state the triple `replication.factor / min.insync.replicas / acks` and what failure it survives.
