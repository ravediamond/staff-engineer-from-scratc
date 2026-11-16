# Week 13: Streaming and messaging (Kafka)

**Everything you need for this week is on this page.** You need week 2 (idempotency), week 3 (replication, fencing) and week 4 (logs, the exactly-once consumer). You do not need to have used Kafka: this page starts from zero. Plain Python; nothing to install for the labs.

"Design the event pipeline" comes up in most system design rounds, and it is one of the two topics you said went badly in past interviews. The fix is to stop treating Kafka as a box with a name and to know what is inside. Everything in Kafka follows from one structure, the log, and a few rules about positions in it. This week you build them one by one, then reproduce the same behaviour on a real Kafka.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Streaming in ten minutes](#streaming-in-ten-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-the-commit-log), [Day 2](#day-2-replication), [Day 3](#day-3-producers-and-consumer-groups), [Day 4](#day-4-stream-processing), [Day 5](#day-5-outbox-schemas-then-a-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w13dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w13dN_*.py` | tests | run, never edit |
| `review_w13dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt) and `rubric.md`. You write your answer in a new file, `my_design.md`. After Wednesday's lab, do the hands-on track in `handson/kafka/` (two sessions of one hour, on a real Kafka in Docker).

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w13-streaming/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w13-streaming/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w13-streaming/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w13-streaming/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-commit-log` | what is a partition, really? | an append-only log with segments, retention and compaction | what compaction does to offsets |
| Tue | `d2-replication` | when is a record safe? | replication with in-sync replicas, the high watermark and acks | where the high watermark comes from |
| Wed | `d3-clients` | how do producers and consumers stay correct? | a partitioner, an idempotent broker, a consumer-group coordinator | who may commit |
| Thu | `d4-stream-processing` | how do you count events that arrive late? | windows, watermarks, checkpoints | how watermarks of several inputs combine |
| Fri | `d5-outbox-design` | how does a service publish events reliably? | the transactional outbox, schema compatibility; then a timed design | the order of two steps |

## Streaming in ten minutes

### Why a log between services

Service A does something that services B, C and D need to know about. Calling each one directly ties A to all of them: if C is down, does A fail? If a new service E arrives, A must change. Instead A **writes an event** ("order 42 was created") to a durable log, and everyone who cares **reads** that log at their own pace. A does not know its readers. A reader that is down catches up later. That is the whole idea of event streaming, and **Kafka** is the standard system for it.

### The words

| Word | Meaning |
|---|---|
| event, record, message | one entry: an optional **key**, a **value**, a timestamp |
| topic | a named stream of records, such as `orders` |
| partition | a topic is split into partitions; **each partition is one ordered, append-only log** |
| offset | the position of a record in its partition: 0, 1, 2… It never changes |
| broker | one Kafka server. A cluster has several |
| producer | a program that writes records |
| consumer | a program that reads records |
| consumer group | consumers that share the work of reading a topic: each partition is read by one member of the group |
| committed offset | how far a group has processed a partition; where it resumes after a restart |
| lag | how far a group is behind: the end of the log minus its committed offset |

```
topic "orders", 3 partitions
  partition 0:  [0][1][2][3][4] →          each partition: its own log, its own offsets
  partition 1:  [0][1][2] →
  partition 2:  [0][1][2][3] →
producer ── key "user-7" ── hash ──▶ always the same partition ──▶ records of one user stay in order
```

### Four facts to keep

1. **Order is guaranteed only inside one partition.** Records with the same key go to the same partition, so they stay ordered. Across partitions there is no order.
2. **Reading does not remove anything.** A consumer is a position in the log. Several groups read the same records independently, and a group can go back and read again (**replay**).
3. **Kafka is a log, not a queue.** There is no "delete this message once handled". Records leave by age or by compaction, whoever has or has not read them.
4. **Delivery is at least once by default.** Duplicates are normal, so consumers are idempotent (week 2).

## Day 1: The commit log

Folder: `d1-commit-log`. Exercise: `w13d1_log.py`.

### One structure

A partition is an **append-only log**. Each new record gets the next offset. Offsets are never reused and never change. Everything else in Kafka (replication, groups, exactly-once) is bookkeeping about offsets in this log.

Appending at the end of a file is the fastest thing a disk does (week 4). That is why one broker moves hundreds of megabytes per second on ordinary disks.

### Segments and the sparse index

On disk a partition is not one endless file. It is cut into **segments** of bounded size. Only the last one, the **active segment**, receives writes; the others are closed and never change.

A segment is named by its **base offset**, the offset of its first record. To read from offset `N`:

1. binary search among the segments for the one whose base offset is the largest that is ≤ `N`;
2. inside it, use the **sparse index**: one entry (offset → position) every few records, not one per record; binary search for the closest entry at or before `N`;
3. scan forward from there.

A sparse index is small enough to stay in memory and costs a short scan. It is the same trade as a bloom filter: a little extra work on reads for a structure that fits in RAM.

### Two ways to clean up

Both apply to **closed** segments only, never to the active one.

**Retention** (`cleanup.policy=delete`). Whole segments are dropped once their **newest** record is older than a limit (seven days by default). The **log start offset** moves forward. A consumer that asks for an offset that no longer exists gets an `OffsetOutOfRange` error.

**Compaction** (`cleanup.policy=compact`). Keep only the **latest record for each key**. A record whose value is empty is a **tombstone**: it means "this key is deleted", and removes the key. Compaction turns a topic into a table you can rebuild by reading it from the start: "the current state of every key".

```
before:  off 0 k=a v=1 | off 1 k=b v=1 | off 2 k=a v=2 | off 3 k=b v=None | off 4 k=c v=1
after:                                   off 2 k=a v=2 |                    off 4 k=c v=1
```

**Offsets of the surviving records do not change.** The log now has gaps (offsets 0, 1 and 3 are gone) and that is normal: readers skip over them. Compaction that renumbers the survivors 0, 1, 2… breaks every consumer: their committed offsets now point at different records. That is today's review bug.

### Traps of the day

- Offsets renumbered after compaction.
- The active segment cleaned.
- Retention decided on the oldest record of a segment instead of the newest: data younger than the limit is deleted.
- A read from a deleted offset returning nothing instead of an error.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `PartitionLog.append` | next offset; roll to a new segment when full; maintain the sparse index | one structure; segments |
| `read` | records from an offset, through segments and index | segments and the sparse index |
| `apply_retention` | drop old closed segments; move the log start | retention |
| `compact` | latest record per key, tombstones removed, offsets kept | compaction |

Run: `uv run pytest weeks/w13-streaming/d1-commit-log -k "not review"`

---

## Day 2: Replication

Folder: `d2-replication`. Exercise: `w13d2_replication.py`.

### The setting

A broker can die. So each partition is stored on several brokers: its **replicas**. One replica is the **leader**: it takes all the writes. The others are **followers**: they **pull** records from the leader and append them to their own copy.

### Four terms carry the whole durability story

| Term | Meaning |
|---|---|
| **LEO**, log end offset | the next offset a replica will write: the length of its log |
| **ISR**, in-sync replicas | the replicas that have kept up with the leader recently. The leader is always in it |
| **HW**, high watermark | the smallest LEO among the ISR members. Everything **below** it is on every in-sync replica: it is **committed** |
| **acks** | what a producer waits for before considering a record sent |

```
leader     LEO 5    [0][1][2][3][4]
follower A LEO 5    [0][1][2][3][4]        in sync
follower B LEO 3    [0][1][2]              in sync, a little behind
HW = min(5, 5, 3) = 3   →  offsets 0, 1, 2 are committed
```

The high watermark is the **minimum over the in-sync replicas**, not the leader's own end. The leader always has the newest records, and those are exactly the ones that may not be anywhere else yet. Taking the leader's LEO as the high watermark declares records committed that a failover can erase. That is today's review bug.

### The rules that follow

**Consumers see only records below the high watermark.** A record above it may disappear if the leader dies before the followers fetch it. A consumer that had read it would have acted on something that, officially, never happened.

**acks**, the producer's choice:

| acks | The producer waits for | Risk |
|---|---|---|
| `0` | nothing | lost if anything goes wrong |
| `1` | the leader to write it | lost if the leader dies before a follower copies it |
| `all` | the record to be below the high watermark | none, as long as one in-sync replica survives |

**`min.insync.replicas`**. With `acks=all`, "all" means all the **current** in-sync replicas, and that set can shrink to the leader alone. `min.insync.replicas=2` says: refuse the write if fewer than 2 replicas are in sync. On 3 replicas with `acks=all` and this setting, an acknowledged write survives the loss of one broker. When too few replicas are in sync, producing fails (`NotEnoughReplicas`): the partition chooses consistency over availability, for writes.

**A new leader is elected from the ISR.** Its log contains everything committed. Electing a replica from outside the ISR (**unclean leader election**) keeps the partition available when no in-sync replica is left, and silently loses committed records. It is off by default.

**After a failover, a replica that has records the new leader does not have cuts them off** (truncates). With `acks=1` those could be records a producer was told were written. That is the data-loss window of `acks=1`, and the sentence to say in a design review.

The interview answer in one line: `acks=all`, replication factor 3, `min.insync.replicas=2`, unclean election off.

### Traps of the day

- High watermark from the leader's end.
- Consumers reading up to the leader's end.
- `acks=all` acknowledged when the ISR is below the minimum.
- A leader elected from outside the ISR with unclean election off.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Partition.produce`, `acked` | append on the leader; is this offset acknowledged under the chosen acks? | acks; `min.insync.replicas` |
| `replicate`, `shrink_isr` | a follower fetches; a slow one leaves the ISR; the high watermark moves | four terms |
| `fetch` | what a consumer may read | consumers see only below the high watermark |
| `fail`, `recover` | leader election, truncation | a new leader; after a failover |

Run: `uv run pytest weeks/w13-streaming/d2-replication -k "not review"`

---

## Day 3: Producers and consumer groups

Folder: `d3-clients`. Exercise: `w13d3_clients.py`.

### The producer side

**Which partition?** `hash(key) % number of partitions`. Same key, same partition, so the records of one key stay in order. The hash must be the same on every machine: `zlib.crc32` of the key's bytes, never Python's `hash()`, which changes from one process to the next.

```python
import zlib
zlib.crc32("user-7".encode()) % 6           # the same answer on every machine, every run
```

**Changing the number of partitions moves most keys** (the modulo problem of week 3, day 1). A key's old records are in one partition and its new ones in another: order for that key is broken across the change. Choose the partition count with room to grow, and say so in a design.

**Retries make duplicates.** A producer sends a record, the acknowledgement is lost, the producer sends it again. The broker now has it twice. The **idempotent producer** fixes that: each producer has an id and numbers its records per partition, 0, 1, 2…. The broker remembers the last number it accepted from each producer:

| Incoming sequence number | The broker |
|---|---|
| last + 1 | accepts it |
| ≤ last | drops it as a duplicate, and **still acknowledges** (the producer must stop retrying) |
| > last + 1 | rejects it: a record is missing, order would be broken |

### The consumer side

Consumers with the same `group.id` form a **group** and share the partitions: each partition belongs to **one** member at a time. Add a member and the work is spread; a member dies and its partitions go to others. That redistribution is a **rebalance**, and each rebalance increases the group's **generation** number.

The **range assignor** is the simplest way to share: sort the members, give each a contiguous block of `partitions // members` partitions, and one more to the first `partitions % members` members.

Two consequences worth saying out loud: a group cannot use more consumers than there are partitions (the extra ones sit idle), so **the partition count caps the parallelism**; and the group's progress is one committed offset per partition, from which **lag** is computed. Lag that keeps growing is the first alert to put on any consumer.

### The zombie consumer

A consumer stalls: a long pause, or a handler that takes ten minutes. The group decides it is dead, rebalances, and gives its partitions to another member, which processes on from the last committed offset. Then the first consumer wakes up, unaware, and **commits its old position**. The committed offset jumps backwards, and the records in between are processed again by whoever reads next.

The coordinator must **reject a commit from an old generation**. It is the fencing token of week 3, day 5: the generation number is the token. Accepting the zombie's commit is today's review bug.

### After today's lab: the real thing

`handson/kafka/README.md`: two sessions of one hour on a real Kafka in Docker. You create a topic, watch the partitioner, kill a broker, watch the ISR shrink and the leader change, and make a consumer group rebalance. Reproduce on the real tool what you simulated this week, and write what you saw in the day's `questions.md`. The guide says it honestly: its commands were written from the documentation and not executed when the repo was generated; when one fails, fixing it is part of the exercise, and asking for help there is allowed.

### Traps of the day

- Python's `hash()` as partitioner.
- A duplicate rejected with an error instead of acknowledged.
- A commit from an old generation accepted.
- More consumers than partitions, expecting more throughput.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `partition_for` | stable partition of a key | the producer side |
| `moved_fraction` | share of keys that move when the partition count changes | the producer side |
| `IdempotentBroker.append` | accept, deduplicate or reject by sequence number | retries make duplicates |
| `range_assign` | share partitions among members | the consumer side |
| `GroupCoordinator` | `join`, `leave`, `commit` with generations, `lag` | the consumer side; the zombie consumer |

Run: `uv run pytest weeks/w13-streaming/d3-clients -k "not review"`

---

## Day 4: Stream processing

Folder: `d4-stream-processing`. Exercise: `w13d4_streams.py`.

### Two clocks

Every event has two times:

- **event time**: when it happened. A field in the record.
- **processing time**: when your job sees it.

Phones go offline, networks retry, queues back up: events arrive late and **out of order**. "Clicks per minute" must mean per minute of **event time**. Counted by processing time, the result changes every time you replay the data, and a backlog shows up as a traffic spike that never happened.

### Windows

A **window** groups events by time. The simplest, a **tumbling** window, cuts time into equal, non-overlapping slices: `[0, 60)`, `[60, 120)`…. An event with event time `t` belongs to the window starting at `t − (t mod size)`.

### Watermarks: deciding that a window is finished

To publish the count for `[0, 60)` you must decide that no more events for it will arrive. Events can be late, so you can never be certain. A **watermark** is the job's working claim: "I believe I have seen everything up to time W."

The usual estimate, per input partition:

```
watermark of a partition = largest event time seen there − the out-of-order delay you tolerate
```

With several partitions, the job's watermark is the **minimum** over them. The slowest partition decides: if partition 2 is still delivering events from 10:00, the job cannot claim to have seen everything up to 10:05 just because partition 0 is already there.

Taking the **maximum** closes windows while a slower partition still holds events for them. Those events are then treated as late and their counts are wrong. That is today's review bug. (The price of the minimum: an **idle** partition holds everything back, which is why real engines have an idle-source timeout.)

### Firing, lateness, the side output

- A window `[start, end)` **fires** (its result is published) when `watermark ≥ end`.
- **Allowed lateness**: its state is kept a while longer, until `watermark ≥ end + lateness`. A late event arriving in that period updates the count, and the window fires **again** with the corrected value: an **update**.
- After that, a late event for the window goes to a **side output** (a dead-letter stream). It is counted and kept somewhere, never dropped in silence.

The three settings are one trade: wait longer for more complete results, or publish sooner and correct.

### Fault tolerance: checkpoints

The job holds state: the open windows and their counts. If it crashes, that state is gone. A **checkpoint** saves the state **together with the input offsets it reflects**. After a crash: restore the state, rewind each input to the saved offsets, and replay from there.

The pairing is the point. State restored with newer offsets loses events; with older offsets it counts some twice. Saved as one unit, the state is correct exactly once.

The **outputs** are another matter: results published between the checkpoint and the crash are published again on replay. They are exactly-once only if the sink is idempotent or transactional. In an interview, say "exactly-once state, and exactly-once output only with an idempotent or transactional sink".

### Traps of the day

- The maximum of the partition watermarks.
- Windows by processing time.
- Late events dropped.
- A checkpoint that saves the state without the offsets.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `WindowedCounter.process` | assign an event to its window; update the partition's watermark; route late events | windows; firing, lateness |
| `watermark` | the job's watermark | watermarks |
| `emit` | the windows that fire, and updates | firing, lateness |
| `snapshot`, `restore` | state and offsets, together | checkpoints |

Run: `uv run pytest weeks/w13-streaming/d4-stream-processing -k "not review"`

---

## Day 5: Outbox, schemas; then a design

Folder: `d5-outbox-design`. Exercise: `w13d5_outbox.py`. Also in the folder: `design.md`, `rubric.md`.

### The dual-write problem

A service saves an order in its database **and** publishes an "order created" event. Those are two systems, and there is no transaction across a database and Kafka. A crash between the two leaves either an order with no event (downstream never hears of it) or an event with no order (downstream acts on something that does not exist). Whatever order you do them in, one of the two can happen.

### The transactional outbox

Write **both** in the database, in **one transaction**: the business row, and a row in an `outbox` table that describes the event to send. A database transaction is atomic: both rows exist, or neither.

A separate process, the **relay**, reads the outbox in order and publishes each row to Kafka, then marks it as published.

```
transaction:  INSERT order 42  +  INSERT outbox(event_id="order-created:42", …)      atomic
relay:        read unpublished rows in order → publish → mark published
```

In production the relay is usually **change data capture**: a tool (Debezium) reads the database's own write-ahead log and turns committed outbox inserts into Kafka records.

**The relay is at-least-once.** Its two steps are "publish" and "mark as published", and a crash can fall between them. The order must be **publish, then mark**: a crash then republishes a row, which is a duplicate, and duplicates are handled. Marking first and then publishing loses the event for good if the crash falls between: nothing will ever send it. That is today's review bug, and it is the consumer table of week 4, day 5 seen from the other side.

So every consumer is **idempotent**: it stores the event id in the same transaction as its own effect and skips an id it has already applied. A stable `event_id` derived from the business key makes that possible.

### Schemas are a contract

Producer and consumer teams deploy at different times. For a while, some programs write the new format while others still read with the old one, or the reverse. A **schema registry** checks every new version of a schema against a compatibility rule before allowing it.

| Mode | Rule | Who upgrades first |
|---|---|---|
| BACKWARD | a reader with the **new** schema can read data written with the **old** one | consumers |
| FORWARD | a reader with the **old** schema can read data written with the **new** one | producers |
| FULL | both | either |

The reasoning is always about a reader meeting a field it does not expect, or missing one it expects. A missing field is fine **if the reader's schema gives it a default**. A field the reader does not know is ignored. A field whose type changed is never fine.

In practice: you may **add a field with a default**, or remove one that had a default. Never change a type, rename a field, or reuse a field's number.

### Sizing a topic

How many partitions? Enough for the target throughput on both sides: `target / throughput of one partition`, and `target / throughput of one consumer` (since a group has at most one consumer per partition). Take the larger, multiply by headroom, round up.

### After the lab: the Friday design (45 minutes, timed)

`design.md` is design number 7 of the repo.

1. Start a 45-minute timer. Write in `my_design.md`, following the 45-minute frame of [week 5](../w5-design-method/README.md#the-45-minute-frame). Stop at the bell.
2. Grade yourself with `rubric.md`.
3. Only then read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
4. Write in `PROGRESS.md` the one thing that would have raised your level.

For any design with events, have these sentences ready: the key and why (ordering); the partition count and why; `acks=all` with `min.insync.replicas=2`; idempotent consumers; the retention or compaction policy; what you alert on (lag).

### Traps of the day

- Marked as published before publishing.
- The order and the outbox row written in two transactions.
- A consumer that is not idempotent behind an at-least-once relay.
- A new required field with no default.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `place_order` | the order and its outbox row, in one transaction | the transactional outbox |
| `relay_once` | publish unpublished rows in order, then mark | the relay is at-least-once |
| `InventoryConsumer.handle` | apply an event once, by event id | idempotent consumers |
| `backward_compatible`, `forward_compatible` | may this schema change be deployed? | schemas are a contract |
| `partitions_needed` | partition count for a throughput | sizing a topic |

SQLite in memory stands in for the database.

Run: `uv run pytest weeks/w13-streaming/d5-outbox-design -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** redo one drill you marked slow in `PROGRESS.md`, from a blank file, timer on, AI fully off.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 13 when you can do these without notes:

- [ ] define topic, partition, offset, broker, consumer group, lag
- [ ] explain segments, the sparse index, retention and compaction, and what happens to offsets
- [ ] define LEO, ISR and high watermark, and give the safe producer and topic settings
- [ ] explain the idempotent producer and the zombie-consumer problem with its fix
- [ ] explain event time, watermarks (and why the minimum), allowed lateness and checkpoints
- [ ] explain the dual-write problem and the outbox, with the order of the relay's two steps
- [ ] say which schema changes are safe
- [ ] describe what you saw when you killed a real broker

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/16-streaming-and-messaging.md`
- The real tool: `handson/kafka/README.md`
- Previous week: [`../w12-mocks/README.md`](../w12-mocks/README.md) · Next: [`../w14-kubernetes/README.md`](../w14-kubernetes/README.md)
