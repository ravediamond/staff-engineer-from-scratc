# Week 3: Distributed systems

**Everything you need for this week is on this page.** You need weeks 1–2 (hashing, invariants, timeouts, injected clocks). Nothing from other folders is required.

One machine is not enough: not enough storage, not enough capacity, and when it dies the service dies. So data is split across machines and copied across machines, and from that moment the copies can disagree, clocks cannot be trusted, and a machine can believe it is in charge when it is not. This week builds the five mechanisms that every design discussion at staff level falls back on.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Distributed systems in ten minutes](#distributed-systems-in-ten-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-consistent-hashing), [Day 2](#day-2-quorum-replication-read-repair), [Day 3](#day-3-lamport-and-vector-clocks), [Day 4](#day-4-raft-log-replication), [Day 5](#day-5-leases-and-fencing-tokens).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w3dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w3dN_*.py` | tests | run, never edit |
| `review_w3dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w3-distributed/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w3-distributed/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w3-distributed/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w3-distributed/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-consistent-hashing` | which machine holds this key? | a hash ring with virtual nodes; rendezvous hashing | the end of the ring |
| Tue | `d2-quorum` | how many copies must answer? | quorum reads and writes with read repair | which version wins |
| Wed | `d3-clocks` | which event came first? | Lamport and vector clocks; sibling versions | how two clocks are merged |
| Thu | `d4-raft-log` | how do copies agree on one history? | Raft log replication and its commit rule | when an entry counts as committed |
| Fri | `d5-leases-fencing` | who holds the lock, really? | a lease service and fenced storage | what the storage remembers |

## Distributed systems in ten minutes

| Word | Meaning |
|---|---|
| node | one machine (or process) of the system |
| partition, shard | a slice of the data; each node holds some slices. Splitting data this way is **sharding** |
| replica | a copy of the same data on another node |
| replication | keeping the replicas in step |
| leader, follower | in many systems one replica (the leader) takes the writes and the others (followers) copy it |
| network partition | some nodes cannot reach the others; each side is alive |
| consistency | here: do all readers see the same, latest data? |
| availability | does the system still answer when nodes are down or cut off? |
| quorum | a number of replicas large enough that any two such groups share at least one member; usually a majority |

Three facts that explain every mechanism of the week:

1. **A slow node and a dead node look the same.** All you have is a timeout.
2. **Clocks on different machines disagree,** by milliseconds usually and by seconds sometimes. "The latest write" by wall-clock time is a guess.
3. **A node can stop for seconds without knowing it** (a garbage-collection pause, a frozen virtual machine) and then resume as if no time had passed.

And one trade-off, the **CAP theorem** in plain words: during a network partition, a system must choose. Either it refuses some requests to stay consistent, or it answers everyone and accepts that the two sides may diverge. It cannot do both.

## Day 1: Consistent hashing

Folder: `d1-consistent-hashing`. Exercise: `w3d1_hashing.py`.

### The problem with modulo

To spread keys over `N` nodes, the obvious rule is `node = hash(key) % N`. It balances well. Its flaw shows when `N` changes: going from 10 to 11 nodes changes the result for about 91% of the keys. Every one of those keys must move, and a cache loses almost everything at once.

### The ring

**Consistent hashing** puts nodes and keys in the same space. Imagine the hash values on a circle. Each node is hashed to a point on the circle. A key is hashed too, and belongs to **the first node found going clockwise** from its point.

```
        0
     N3 ·  · k1 → belongs to N1 (next node clockwise)
   ·          · N1
   ·          ·
     N2 ·  · k2 → belongs to N2
```

Add a node: it takes only the keys between its predecessor and itself, all from one neighbour. About `1/(N+1)` of the keys move. Remove a node: its keys go to the next node. Nothing else changes.

In code the ring is a **sorted list** of points. Finding the owner of a key is a binary search for the first point at or after the key's hash, and **past the last point you wrap to index 0**: the circle closes.

```python
import bisect
points = [10, 40, 80]                       # sorted hash positions of the nodes
i = bisect.bisect_left(points, 95)          # 3: past the end
points[i % len(points)]                     # 10: wrap to the first node
```

**Invariant:** the list of points stays sorted, and a lookup returns the first point with `hash ≥ h(key)`, wrapping.

### A hash that does not change between runs

Python's `hash()` of a string changes each time Python starts. A ring must give the same answer on every machine and every run, so it uses a stable hash:

```python
import hashlib
int.from_bytes(hashlib.md5("node-a".encode()).digest()[:8], "big")       # the same number everywhere
```

### Virtual nodes

With one point per node, the arcs between points have very different lengths, so some nodes hold far more keys than others. And when a node leaves, its whole load lands on one neighbour.

**Virtual nodes** give each physical node many points, by hashing `"node#0"`, `"node#1"`, …. With `V` points per node the load evens out (the spread shrinks roughly like `1/√V`), and a departing node's keys are shared among many nodes. The ring then needs to remember which physical node each point belongs to.

### Rendezvous hashing

No ring. For a key, compute a score `hash(node, key)` for every node and pick the node with the **highest** score. When a node leaves, only its keys move, each to its second-best node. It costs O(N) per lookup, which is fine for a small number of nodes.

### Two measures

- **Moved fraction** between two assignments: among keys present in both, the share whose owner changed.
- **Imbalance**: keys on the busiest node divided by the mean number of keys per node. 1.0 is perfect.

### Traps of the day

- No wrap-around: keys past the last point crash or all go to one place.
- Python's built-in `hash`.
- Removing a node but leaving some of its virtual points.
- The points list no longer sorted after an insertion.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `stable_hash` | the same integer in every process | a hash that does not change |
| `Ring` | `add`, `remove`, `lookup`, `assignment`, with virtual nodes | the ring; virtual nodes |
| `rendezvous` | highest score wins | rendezvous hashing |
| `moved_fraction`, `max_over_mean` | movement and imbalance | two measures |

Run: `uv run pytest weeks/w3-distributed/d1-consistent-hashing -k "not review"`

---

## Day 2: Quorum replication, read repair

Folder: `d2-quorum`. Exercise: `w3d2_quorum.py`.

### Three numbers

Each key is stored on **N** replicas. A write is sent to the replicas and counts as successful once **W** of them have acknowledged it. A read asks **R** replicas and returns the value with the **highest version**.

Some replicas may be down or slow, so the replicas do not all hold the same thing. The rule that still gives correct reads:

```
R + W > N
```

Then any group of `R` replicas and any group of `W` replicas share at least one member. So among the replicas a read asks, at least one took part in the latest successful write, and the highest version the read sees is that write.

| N, R, W | What you get |
|---|---|
| 3, 2, 2 | reads see the latest acknowledged write; one node may be down for reads and for writes |
| 3, 1, 3 | fast reads; a write needs every replica up |
| 3, 1, 1 | fast and always available; **stale reads possible** (1 + 1 is not more than 3) |

With N = 3, W = 2, R = 2: a write reaches replicas {0, 1}; a later read asks {1, 2}; replica 1 is in both and has the new value.

### Partial writes stay

A write that reaches fewer than `W` replicas is reported as **failed**, and the replicas that did receive it **keep it**. There is no rollback. A later read may or may not see it. "The write failed" means "not guaranteed", not "did not happen". This surprises people, and interviewers ask about it.

### Read repair

A read has just seen which of the replicas it asked hold an old version, or nothing. It writes the newest version back to them before returning. Data that is read gets healed for free. Keys nobody reads are repaired by a background comparison process (anti-entropy).

### Versions

Today a version is a number given by the client, such as a timestamp, and the highest wins: **last writer wins**. That rule is only as good as the clocks. Tomorrow shows what it loses.

### Traps of the day

- Returning the first answer instead of the highest version.
- Read repair written to every replica, or with the stale value.
- A failed write rolled back in the simulation: real systems do not.
- A quorum counted over all replicas instead of the ones that are up and were asked.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `overlaps` | does every read quorum meet every write quorum? | three numbers |
| `Cluster.put` | write to the targets that are up; `QuorumError` below `W`; partial writes persist | partial writes stay |
| `Cluster.get` | read `R` replicas; highest version; repair the stale ones | read repair |

Run: `uv run pytest weeks/w3-distributed/d2-quorum -k "not review"`

---

## Day 3: Lamport and vector clocks

Folder: `d3-clocks`. Exercise: `w3d3_clocks.py`.

### Why not wall-clock time

Two machines write the same key at nearly the same moment. Machine B's clock is 200 ms behind. Its write, which really happened later, carries the smaller timestamp, and last-writer-wins throws it away. Nothing reports an error. Data is lost silently.

**Logical clocks** do not measure time. They track **causality**: could this event have influenced that one?

### Lamport clocks

One counter per process.

- Before each local event, and before sending a message: add 1. The message carries the counter.
- On receiving a message with timestamp `t`: `counter = max(counter, t) + 1`.

Guarantee: if event A could have influenced event B, then `L(A) < L(B)`. The reverse is **not** true: a smaller number does not mean "happened before". Two unrelated events on two machines get numbers that compare by accident. A Lamport clock gives an order consistent with causality; it cannot detect that two events were independent.

### Vector clocks

Each process keeps one counter **for every process**: a small dict.

- On a local event: add 1 to your own entry.
- On receive: for every entry take the larger of the two values, then add 1 to your own entry.

The merge is **entry by entry**. Keeping whichever whole clock looks "bigger" throws away what the other one knew: `{A:3, B:0}` and `{A:0, B:2}` must merge to `{A:3, B:2}`, not to either of them. That is today's review bug.

A vector clock summarises "everything I have heard of". Comparing two of them, entry by entry (a missing entry counts as 0):

| Result | Condition | Meaning |
|---|---|---|
| equal | every entry equal | the same event |
| a before b | every entry of `a` ≤ the entry of `b`, at least one smaller | `b` knew about `a` |
| a after b | the reverse | |
| **concurrent** | `a` is larger somewhere **and** `b` is larger somewhere | neither knew of the other: a **conflict** |

```
A writes:            {A:1}
B writes, unaware:   {B:1}            compare {A:1} with {B:1} → concurrent
C merges both:       {A:1, B:1, C:1}  after both
```

### Siblings

A store that uses vector clocks does not pick a winner between concurrent versions. It keeps **all** of them, the **siblings**, and hands them to the application, which knows how to merge: a shopping cart takes the union of the items.

To compute the siblings of a set of versions: drop every version that is strictly **before** some other version (it is obsolete), and keep one copy of versions with equal clocks.

Today's functions are **pure**: they return new dicts and never modify their arguments.

### Traps of the day

- Receive that takes the max and forgets the `+ 1` (or the increment of the own entry).
- Missing entries not treated as 0.
- "Concurrent" reported as "before" because only one direction was checked.
- A function that modifies the dict it was given.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `LamportClock` | `tick`, `send`, `receive` | Lamport clocks |
| `vc_increment`, `vc_merge` | own entry + 1; element-wise maximum | vector clocks |
| `vc_compare` | equal, before, after or concurrent | vector clocks |
| `siblings` | the versions that no other version supersedes | siblings |

Run: `uv run pytest weeks/w3-distributed/d3-clocks -k "not review"`

---

## Day 4: Raft log replication

Folder: `d4-raft-log`. Exercise: `w3d4_raft.py`.

### The problem: one history for everyone

Several replicas must apply the **same commands in the same order**, even when messages are lost and nodes crash. If they do, they end in the same state. Agreeing on that order is **consensus**, and **Raft** is the consensus algorithm designed to be understood. etcd (the store behind Kubernetes) and many databases use it.

### The pieces

- **The log**: an ordered list of entries. Each entry is `(term, command)`. Positions are numbered from 1.
- **A term**: a period with one leader. Terms are numbered 1, 2, 3… A new election starts a new term. The term works as a logical clock: a message from an older term comes from a leader that has been replaced.
- **The leader** receives the clients' commands, appends them to its own log, and sends them to the followers with a message called **AppendEntries**.
- **Committed**: an entry is committed when it is certain never to be lost. Only committed entries are applied.

Today covers replication, not elections.

### Rule 1, on the follower: the logs must match before appending

The leader does not just send new entries. It also says what comes **just before** them in its own log: `prev_index` and `prev_term`.

```
AppendEntries(term, prev_index, prev_term, entries, leader_commit)
```

The follower:

1. **Rejects** if `term` is smaller than its own current term: a stale leader.
2. **Rejects** if it has no entry at `prev_index` with term `prev_term`: its log differs from the leader's somewhere before this point. (Index 0 is a fake entry with term 0 that always matches, so the very first append works.)
3. Otherwise goes through the new entries. If it already has an entry at that index with a **different term**, that entry and **everything after it** are deleted, then the new entry is appended. If it already has the same entry, it keeps it: messages can arrive twice or out of order.
4. Updates its commit index to `min(leader_commit, index of the last new entry)`.

On a rejection the leader steps back one entry for that follower and tries again, until it finds the point where the two logs agree. From there it overwrites the follower's log with its own. A follower's uncommitted entries from an old leader can be thrown away; that is safe precisely because they were not committed.

The leader keeps two numbers per follower: `next_index`, the next entry to send, and `match_index`, the highest entry known to be stored there.

### Rule 2, on the leader: when is an entry committed?

"Stored on a majority" is almost the answer. The exact rule: the leader advances its commit index to the highest `N` such that

- a majority of nodes (the leader included) has `match_index ≥ N`, **and**
- **`log[N].term` is the leader's current term.**

An entry from an **older** term is never committed by counting copies. It becomes committed indirectly, when an entry of the current term placed after it is committed.

Why the second condition: an entry of an old term can sit on a majority and still be overwritten later by a leader that never saw it (the scenario of Figure 8 of the Raft paper). An entry of the current term on a majority cannot, because any node that could win the next election must have it. Skipping the term check is today's review bug, and the most asked detail of Raft.

A majority of 5 nodes is 3. With `match_index` values sorted, the middle one is the highest index a majority holds.

### Traps of the day

- No check of `prev_index` and `prev_term`: logs silently diverge.
- Truncating the log whenever entries arrive, even when they match: a delayed duplicate message deletes newer entries.
- Commit index set to `leader_commit` without the `min`.
- Counting copies of an old-term entry.
- Off-by-one between 1-based log positions and 0-based Python lists.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Follower.append_entries` | the four steps; returns `(success, match_index)` | rule 1 |
| `Leader.request_for` | build the AppendEntries arguments for one follower | rule 1 |
| `Leader.on_response` | move `next_index` and `match_index` forward, or step back | rule 1 |
| `Leader.advance_commit` | the commit rule with the term check | rule 2 |
| `replicate_until_stable` | keep sending until nothing changes | — |

Run: `uv run pytest weeks/w3-distributed/d4-raft-log -k "not review"`

---

## Day 5: Leases and fencing tokens

Folder: `d5-leases-fencing`. Exercise: `w3d5_fencing.py`.

### A lock across machines is a lease

On one machine a lock is held until released. Across machines the holder may crash and never release it. So a distributed lock is given for a limited time: a **lease**. The holder must renew it before it expires, or someone else may take it.

### Why a lease alone is unsafe

Fact 3 from the top of the page: a process can stop for a long time without knowing.

```
client A:  acquire ──── [ paused 40 s ............ ] ──── write   ← A believes it still holds the lock
lock svc:        lease of A expires ── client B acquires ── B writes
```

A wakes up. From its point of view no time has passed. It writes. Now two clients have written under "the" lock. A cannot prevent this by checking the clock first: it could be paused between the check and the write.

### The fix: fencing tokens

The lock service gives a **number** with every grant, and the number only ever increases. The **storage** remembers the highest number it has accepted for each resource and **rejects** any write that carries a lower one.

```
A acquires, token 33 ── pause ──────────────────────── write(token 33) → REJECTED: 33 < 34
B acquires, token 34 ── write(token 34) → accepted, the storage now remembers 34
```

A storage that does not remember the highest token it has seen cannot reject anything. That is today's review bug.

Safety has moved. It no longer depends on the client knowing whether its lease is valid, which is impossible. It depends on the resource comparing two numbers, which is easy. The lock is only as safe as the check done by whatever it protects.

Rules of the lock service: a grant is refused while another client's lease is valid; a token is handed out on **every** grant, including a new grant to the same client after its lease expired; renew and release work only for the current holder with the current token.

### Traps of the day

- Storage that accepts any token.
- A token reused when the same client acquires again after expiry.
- Renewal accepted for an expired lease or an old token.
- Expiry compared with `<` where the lease boundary needs `<=`: the docstring gives the convention.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `LockService` | `acquire`, `renew`, `release`, with increasing tokens and an injected clock | a lease; the rules |
| `FencedStorage.write` | accept only tokens at least as high as the highest seen; else `StaleToken` | fencing tokens |
| `simulate_gc_pause` | the scenario of the diagram, end to end | why a lease alone is unsafe |

Run: `uv run pytest weeks/w3-distributed/d5-leases-fencing -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w03`, timer on, AI fully off: `uv run pytest drills/w03 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 3 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 3 when you can do these without notes:

- [ ] explain why modulo hashing fails and how a ring with virtual nodes fixes it
- [ ] explain `R + W > N` with an example, and what happens to a failed write
- [ ] compare two vector clocks and say what "concurrent" means for the application
- [ ] state the two rules of Raft log replication, with the term check and why
- [ ] explain why a lease cannot be made safe by the client, and how a fencing token fixes it
- [ ] state the three facts and the CAP trade-off in your own words

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/03-distributed-systems.md`
- Previous week: [`../w2-reliability/README.md`](../w2-reliability/README.md) · Next: [`../w4-storage-retrieval/README.md`](../w4-storage-retrieval/README.md)
