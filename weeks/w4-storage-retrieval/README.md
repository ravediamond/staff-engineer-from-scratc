# Week 4: Storage and retrieval

**Everything you need for this week is on this page.** You need week 1 (heaps, hash maps, caches), week 2 (idempotency, asyncio) and week 3. Thursday uses numpy. Nothing from other folders is required.

Under every system there is something that stores data and something that finds it again. This week opens both boxes: how a database survives a crash and why writes are fast (the engine under RocksDB, Cassandra and most vector databases), then the two ways to find text (keywords and vectors) that week 6 combines into RAG, then the cache and the consumer that sit in front of every store.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Storage in five minutes](#storage-in-five-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-write-ahead-log-and-lsm-tree), [Day 2](#day-2-bloom-filters-and-compaction), [Day 3](#day-3-inverted-index-and-bm25), [Day 4](#day-4-vector-search), [Day 5](#day-5-cache-aside-single-flight-exactly-once-consumer).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w4dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w4dN_*.py` | tests | run, never edit |
| `review_w4dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w4-storage-retrieval/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w4-storage-retrieval/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w4-storage-retrieval/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w4-storage-retrieval/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | You learn | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-wal-lsm` | durability; the LSM tree | a write-ahead log and a small LSM store with recovery | the search order on reads |
| Tue | `d2-bloom-compaction` | skipping files; merging files | a bloom filter and a compaction | which version survives a merge |
| Wed | `d3-bm25` | keyword search | an inverted index with BM25 scoring | the length normalisation |
| Thu | `d4-vector-search` | search by meaning | exact search, IVF, a graph index, recall@k | a missing normalisation |
| Fri | `d5-cache-consumers` | caching and consuming correctly | a single-flight cache; an exactly-once consumer | the order of two steps |

## Storage in five minutes

- **Memory (RAM)** is fast and is lost when the process stops. **Disk** is slower and survives. A store keeps its working state in memory and must get every change onto disk before saying "done". That promise is **durability**.
- **Sequential writes are cheap; random writes are expensive.** Appending at the end of a file is the fastest thing a disk does. Changing bytes in the middle of many files is slow. Much of storage design is turning random writes into appends.
- **A crash can happen between any two instructions,** including in the middle of writing one record. Storage code is correct only if it is correct after a crash at every such point.
- **An index** is an extra structure that answers "where is it?" without reading everything. It costs space and write time, and it pays back on reads.

## Day 1: Write-ahead log and LSM tree

Folder: `d1-wal-lsm`. Exercise: `w4d1_lsm.py`.

### The write-ahead log (WAL)

The rule: **before changing anything in memory, append a description of the change to a file on disk.** After a crash, read the file from the start and re-apply every record: the memory state is rebuilt. This is how nearly every database gets durability.

One record per line, as JSON, flushed to disk after each append.

A crash can cut the **last** record in half: `{"op": "put", "key": "a", "va`. On replay, that last line does not parse. It was never acknowledged to anyone, so it is safe to ignore it. A broken record anywhere **else** is real corruption and must not be skipped quietly.

```python
import json
lines = ['{"k": "a", "v": 1}', '{"k": "b", "v"']         # the second line is torn
out = []
for i, line in enumerate(lines):
    try:
        out.append(json.loads(line))
    except json.JSONDecodeError:
        if i != len(lines) - 1:
            raise                                          # only the tail may be torn
out                                                        # [{'k': 'a', 'v': 1}]
```

### The LSM tree

A **log-structured merge tree** is a storage engine built from appends only. It is the engine of LevelDB, RocksDB and Cassandra.

```
put / delete ──▶ WAL (append) ──▶ memtable (a dict in memory)
                                     │ when it reaches its limit: flush
                                     ▼
                  SSTables on disk:  [newest] [older] [oldest]
```

- **Memtable**: recent writes, in memory. Protected by the WAL.
- **Flush**: when the memtable is full, write it to a new file, sorted by key. Such a file is an **SSTable** (sorted string table) and is **immutable**: never modified afterwards. Once the flush is safely on disk, the WAL is no longer needed for those writes and is emptied.
- **Read**: look in the memtable, then in the newest SSTable, then the next, down to the oldest. **The first hit wins.**

**Invariant:** for any key, the most recent write is the first one found in that search order.

### Deletes are writes

Files are immutable, so a key cannot be removed from an old SSTable. A delete writes a special value, a **tombstone**, as the newest version of the key. A read that finds a tombstone first answers "absent" and **stops there**. Searching further would find the old value and bring a deleted key back to life.

### Recovery

A new store opened on the same directory must end in the state the old one had: load the SSTables that exist, in the right order, then replay the WAL into a fresh memtable. File names carry a number so the order of creation is known. Sort by that number as an integer: as text, `"sst-10"` comes before `"sst-9"`.

### The trade

Writes are appends: fast on any disk. A read may have to look in several files. Tomorrow's two tools reduce that cost. A B-tree, the engine of PostgreSQL, makes the opposite trade: faster reads, slower writes (week 15).

### Traps of the day

- Memory changed before the WAL append: a crash loses an acknowledged write.
- Reads from oldest to newest.
- A tombstone treated as "not found here, keep looking".
- The WAL not emptied after a flush: recovery re-applies old writes on top of newer files.
- File numbers sorted as text.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `WAL` | `append`, `replay` (ignores a torn last line), `truncate` | the write-ahead log |
| `LSM.put`, `delete`, `get` | WAL first; newest version wins; tombstones | the LSM tree; deletes are writes |
| `LSM.flush` | memtable → a new sorted file, automatically at the limit | the LSM tree |
| recovery | a new `LSM` on the same directory | recovery |

Run: `uv run pytest weeks/w4-storage-retrieval/d1-wal-lsm -k "not review"`

---

## Day 2: Bloom filters and compaction

Folder: `d2-bloom-compaction`. Exercise: `w4d2_bloom.py`.

### The problem

Yesterday's read may open every SSTable to conclude that a key does not exist. Two fixes: know quickly that a file **cannot** contain the key, and have fewer files.

### Bloom filter

A small structure that answers "is `x` in the set?" with **"definitely not"** or **"maybe"**. It uses a few bits per item, whatever the size of the items.

An array of `m` bits, all 0, and `k` hash functions. To **add** an item, compute its `k` positions and set those bits to 1. To **check** an item, look at its `k` positions: if any bit is 0, the item was never added. If all are 1, it probably was, or other items happened to set those bits: a **false positive**.

```
m = 10, k = 2
add "cat" → positions 2, 7     0 0 1 0 0 0 0 1 0 0
add "dog" → positions 4, 7     0 0 1 0 1 0 0 1 0 0
check "cow" → 2, 4: both 1 → "maybe"          a false positive
check "fox" → 1, 7: bit 1 is 0 → "definitely not"
```

**No false negatives, ever.** That is the property the store relies on: "definitely not" lets a read skip the file safely. A false positive only costs one useless file read.

The numbers, for `n` items and a target false-positive rate `p`:

```
false-positive rate   p ≈ ( 1 − e^(−k·n/m) )^k
best size             m = −n · ln(p) / (ln 2)²          about 9.6 bits per item for 1%, 14.4 for 0.1%
best number of hashes k = (m / n) · ln 2
```

Ten bits per item for 1% is worth remembering.

**`k` positions from two hashes.** Computing `k` independent hashes is slow. Take two numbers `h1` and `h2` from one strong hash and use `h1 + i·h2 mod m` for `i = 0 … k−1`.

```python
import hashlib
d = hashlib.sha256(b"cat").digest()
h1 = int.from_bytes(d[:8], "big"); h2 = int.from_bytes(d[8:16], "big")
[(h1 + i * h2) % 1000 for i in range(3)]          # three positions in a filter of 1000 bits
```

### Compaction

Over time there are many SSTables, holding several versions of the same keys and tombstones for keys that are gone. **Compaction** merges several sorted files into one and keeps, for each key, only its **newest** version.

The inputs are sorted, so this is a merge of sorted lists (week 1's heap). When the same key appears in several runs, the version from the **newest run** wins. The runs are given newest first: carry the index of the run with each item and prefer the smallest index.

**Tombstones** can be dropped only when merging into the **bottom** level, where nothing older exists. Dropped earlier, an older file still holding the old value would make the deleted key visible again.

### Traps of the day

- A filter that can answer "no" for an item that was added: a wrong position, or bits not all checked.
- The oldest version kept in a merge.
- Tombstones dropped in a partial compaction.
- `m` rounded down, or `k = 0`.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `optimal_params` | `m` and `k` for `n` items at rate `p` | the numbers |
| `false_positive_rate` | the formula | the numbers |
| `BloomFilter` | `add`, `might_contain`, double hashing | bloom filter |
| `compact` | sorted runs, newest first → one sorted run | compaction |

Run: `uv run pytest weeks/w4-storage-retrieval/d2-bloom-compaction -k "not review"`

---

## Day 3: Inverted index and BM25

Folder: `d3-bm25`. Exercise: `w4d3_bm25.py`.

### The inverted index

To find the documents that contain a word, reading every document is O(all the text). An **inverted index** is built once and answers directly: for each **term**, the list of documents that contain it, with how many times. Such a list is the term's **postings**.

```
doc 1: "the red brick"        brick → {1: 1, 3: 2}
doc 2: "the blue plate"       red   → {1: 1}
doc 3: "brick on brick"       the   → {1: 1, 2: 1}
```

A query only touches the postings of its own terms.

**Tokenising** turns text into terms: lower-case, then keep runs of letters and digits.

```python
import re
re.findall(r"[a-z0-9]+", "Red-brick #42, RED!".lower())      # ['red', 'brick', '42', 'red']
```

### BM25

A ranking formula: how well does document `D` match query `Q`? It is the default of Lucene and Elasticsearch, and still a strong baseline. The score is a sum over the query terms:

```
score(D, Q) = Σ over terms t of Q:   IDF(t) · tf · (k1 + 1) / ( tf + k1 · (1 − b + b · |D| / avgdl) )

IDF(t) = ln( (N − df + 0.5) / (df + 0.5) + 1 )
```

| Symbol | Meaning |
|---|---|
| `tf` | term frequency: how many times `t` occurs in `D` |
| `df` | document frequency: how many documents contain `t` |
| `N` | number of documents |
| `\|D\|`, `avgdl` | length of `D` in terms; average document length |
| `k1`, `b` | two settings, usually about 1.5 and 0.75 |

Three ideas are packed in it:

1. **Rare terms matter more.** `IDF` is large when few documents contain the term. "the" is everywhere and is worth almost nothing.
2. **Repetition saturates.** The `tf` part grows with `tf` and flattens: the tenth occurrence adds far less than the first. `k1` sets how fast.
3. **Long documents are discounted.** A long document contains more of every word by chance. When `|D| / avgdl` is above 1, the denominator grows and the score goes **down**. `b` sets how strongly; `b = 0` turns it off.

After any change to the formula, check the three directions by hand: rarer term, higher score; more occurrences, higher score, less and less; longer document, lower score.

### Boolean AND

"Documents containing **all** the query terms" is the intersection of the postings. Start from the **shortest** list and test its documents against the others: the cost is bounded by the rarest term.

### Order of results

Sort by score, highest first; for equal scores, by document id. A fixed tie-break makes results reproducible, which matters as soon as you evaluate a retriever (week 6).

### Traps of the day

- Length normalisation inverted: long documents win.
- `avgdl` not updated as documents are added.
- A query term absent from the index crashing instead of contributing zero.
- A document indexed twice counted twice in `df`.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `tokenize` | lower-case, runs of `[a-z0-9]` | the inverted index |
| `InvertedIndex.add`, `df`, `avgdl`, `idf` | postings and the statistics | the inverted index; BM25 |
| `bm25` | top `k` `(doc_id, score)` | BM25; order of results |
| `search_and` | documents with every term | boolean AND |

Run: `uv run pytest weeks/w4-storage-retrieval/d3-bm25 -k "not review"`

---

## Day 4: Vector search

Folder: `d4-vector-search`. Exercise: `w4d4_vectors.py`.

### Search by meaning

A keyword index cannot match "car" with "automobile". An **embedding model** turns a text (or an image) into a vector of a few hundred to a few thousand numbers, built so that things with similar meaning get vectors that point in similar directions. Searching by meaning becomes: find the stored vectors closest to the query vector, the **nearest neighbours**.

### Cosine similarity

The usual closeness is the cosine of the angle between two vectors: 1 for the same direction, 0 for unrelated. It equals the dot product **once both vectors are scaled to length 1**.

```python
import numpy as np
X = np.array([[3.0, 4.0], [1.0, 0.0]])
Xn = X / np.linalg.norm(X, axis=1, keepdims=True)       # each row now has length 1
Xn @ np.array([1.0, 0.0])                               # cosine of each row with the query: [0.6, 1.0]
```

Without that scaling, a dot product rewards **long** vectors whatever their direction. It is the most common bug in retrieval code, and today's review bug. A zero vector has no direction: leave it at zero instead of dividing by zero.

### Exact search and why it does not scale

Compare the query with every vector: O(N · d). `np.argsort(-scores)[:k]` gives the best `k`. It is exact, and it is the **ground truth** for everything else. At 100 million vectors of 1 024 floats, one query reads 400 GB. So real systems use **approximate** nearest-neighbour (ANN) indexes: much faster, and sometimes they miss a true neighbour.

### Recall@k: the price of approximation

```
recall@k = | approximate top k ∩ exact top k | / k         averaged over queries
```

Every claim about a vector index is a pair: a recall and a latency, measured on **your** data.

### IVF: search only the nearby cells

**Build.** Group the vectors into `nlist` clusters with **k-means**: pick `k` vectors as starting centres; repeat: assign every vector to its closest centre, then move each centre to the mean of its vectors. With cosine similarity the mean is re-scaled to length 1 (spherical k-means). Each cluster is a **cell**, and each cell keeps the list of its vectors.

**Search.** Compare the query with the `nlist` centres, pick the `nprobe` closest cells, and compare the query only with the vectors in those cells.

`nprobe` is the knob: 1 is fastest and misses neighbours that sit just across a cell border; `nprobe = nlist` is exact search again.

### Graph index: walk toward the query

**Build.** Link every vector to its `M` most similar vectors. The vectors are nodes of a graph.

**Search.** Start at an entry node. Keep a list of the best `ef` candidates found so far. Repeatedly take the best candidate not yet expanded, look at its neighbours, and add those that improve the list. Stop when the best unexpanded candidate is worse than everything in the list. It is a best-first walk that moves, hop by hop, toward the query.

`ef` is the knob: a larger beam explores more and finds more.

**The islands problem.** If every node links only to its nearest neighbours, a dataset made of clusters becomes separate islands with no path between them, and a search that starts on the wrong island never leaves it. A few **random long-range links** per node connect the islands. After your tests pass, set `n_random=0` and watch recall collapse. The production algorithm, HNSW, solves the same problem with sparse upper layers that act as highways.

### Traps of the day

- Vectors or the query not normalised.
- Recall computed against the approximate result itself.
- An empty cell in k-means producing a division by zero.
- A graph search that stops at the first local best with `ef = 1` and is reported as "the index is bad".

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `normalize` | rows scaled to length 1; zero stays zero | cosine similarity |
| `exact_topk` | ground truth | exact search |
| `kmeans` | spherical k-means | IVF |
| `IVFIndex` | `fit`, `search(q, k, nprobe)` | IVF |
| `KNNGraphIndex` | `fit`, `search(q, k, ef)` | graph index |
| `recall_at_k` | the measure | recall@k |

Run: `uv run pytest weeks/w4-storage-retrieval/d4-vector-search -k "not review"`

---

## Day 5: Cache-aside, single-flight, exactly-once consumer

Folder: `d5-cache-consumers`. Exercise: `w4d5_cache_consumer.py`.

### Cache-aside

The most common way to use a cache: read the cache; on a **miss**, load from the source of truth (the database), store the result in the cache with a time to live, return it. Two things go wrong in production.

### Failure 1: the stampede

A very popular key expires. In the next millisecond 5 000 requests all miss, and all 5 000 query the database for the same thing. The database falls over; the cache it was supposed to protect it with made things worse.

**Single-flight**: for each key, only the **first** miss loads. The others wait for that same load and share its result.

In asyncio the shared thing is the **task** doing the load. Keep a dict of loads in progress; a request that finds one there awaits it instead of starting its own.

```python
import asyncio

async def demo():
    calls = 0
    async def load():
        nonlocal calls
        calls += 1
        await asyncio.sleep(0.01)
        return "value"
    task = asyncio.ensure_future(load())               # ONE load in progress
    results = await asyncio.gather(*(asyncio.shield(task) for _ in range(5)))   # five waiters share it
    return calls, results

asyncio.run(demo())                                    # (1, ['value', 'value', 'value', 'value', 'value'])
```

When the load ends, successfully or not, its entry must leave the dict of loads in progress, or a failed load is shared forever.

### Failure 2: stale data after a write

When the data changes, the standard order is: **write the database, then delete the cache key.** Delete, not set. Two writers that each set the cache can interleave so that the older value is the one left in the cache; a delete cannot leave a wrong value, only a miss.

### An exactly-once consumer

A **consumer** reads messages from a log, one position (**offset**) after another, and for each one produces an effect: add an amount to a total, send an email. It records how far it got by **committing** the offset. After a crash it restarts from the committed offset.

There are two steps per message, and a crash can fall between them:

| Order | Crash between the two | Result |
|---|---|---|
| commit the offset, then process | the message is never processed | **lost**: at-most-once |
| process, then commit the offset | the message is processed again after restart | **duplicate**: at-least-once |

There is no third order. Getting the effect exactly once takes at-least-once delivery **plus** an idempotent effect (week 2): the place that stores the effect also stores the ids of the messages already applied, **in the same atomic step** as the effect, and skips an id it has seen. In a real system that is one database transaction that updates the total and inserts the message id.

If the id and the effect are stored in two separate steps, a crash between them brings the duplicate back.

### Traps of the day

- Every miss starting its own load.
- A finished or failed load left in the in-progress dict.
- Commit before process.
- The "already applied" check done in the consumer's memory, which is lost in the crash, instead of in the sink.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `SingleFlightCache` | async `get`; concurrent misses share one load; TTL; a `loads` counter | cache-aside; the stampede |
| `Sink.apply` | add the amount once per message id | an exactly-once consumer |
| `Consumer.run` | process from the committed offset; simulated crash after an effect; resumable | an exactly-once consumer |

Run: `uv run pytest weeks/w4-storage-retrieval/d5-cache-consumers -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w04`, timer on, AI fully off: `uv run pytest drills/w04 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 4 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 4 when you can do these without notes:

- [ ] explain a write-ahead log and what happens to a torn last record
- [ ] draw the write path and the read path of an LSM tree, with tombstones
- [ ] explain a bloom filter, its one guarantee, and "ten bits per item for 1%"
- [ ] say what compaction keeps and when tombstones may be dropped
- [ ] write the BM25 formula and explain its three ideas
- [ ] explain IVF and graph search, each with its knob, and define recall@k
- [ ] explain a cache stampede and single-flight; "write the database, delete the key"
- [ ] explain why exactly-once is at-least-once plus an atomic, idempotent effect

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/04-storage-and-retrieval.md`
- Previous week: [`../w3-distributed/README.md`](../w3-distributed/README.md) · Next: [`../w5-design-method/README.md`](../w5-design-method/README.md)
