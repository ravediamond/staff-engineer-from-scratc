# Week 15: Databases

**Everything you need for this week is on this page.** You need week 2 (idempotency), week 3 (replication, fencing) and week 4 (the LSM tree, to compare with). You need only basic SQL (`SELECT … FROM … WHERE`); the rest is on this page. Plain Python with SQLite, which ships with Python.

Almost every system you will design has a relational database in the middle, and almost every incident you will debug passes through it. Five questions cover what a staff engineer is expected to answer without hesitating: what two concurrent transactions can do to each other, why a query is slow, how to write the SQL an interviewer puts in front of you, what a read replica can show a user, and how to handle money.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Databases in ten minutes](#databases-in-ten-minutes).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-mvcc-and-isolation-levels), [Day 2](#day-2-btree-and-index-choice), [Day 3](#day-3-sql-under-pressure), [Day 4](#day-4-replication-as-the-application-sees-it), [Day 5](#day-5-money).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w15dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w15dN_*.py` | tests | run, never edit |
| `review_w15dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w15-databases/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w15-databases/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w15-databases/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w15-databases/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | The question | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-mvcc` | what can two concurrent transactions see and break? | a multi-version store with snapshots and isolation levels | what a snapshot may see |
| Tue | `d2-btree-indexes` | why is this query slow, and which index fixes it? | a B+tree; rules for composite and covering indexes | a range scan across leaves |
| Wed | `d3-sql` | can you write the query, live? | six queries on a small schema, and one index | a `NULL` |
| Thu | `d4-replication-app-side` | what does a user see when reads go to replicas? | session-aware read routing and a failover | how a replica is chosen |
| Fri | `d5-money` | how do you never lose a cent? | a double-entry ledger, seat holds, a reconciliation | the type of an amount |

## Databases in ten minutes

| Word | Meaning |
|---|---|
| table, row, column | data in a relational database: a table is a set of rows with the same columns |
| primary key | the column (or columns) that identifies a row |
| index | an extra structure that finds rows by a column without reading the whole table |
| query plan | how the database decided to run a query: which index, in which order |
| transaction | a group of reads and writes treated as one unit |
| commit, abort | make a transaction's changes permanent; or cancel all of them |
| ACID | the four promises of a transaction: **a**tomic (all or nothing), **c**onsistent (rules hold), **i**solated (concurrent transactions do not see each other's half-done work), **d**urable (committed means it survives a crash) |
| isolation level | how strictly "isolated" is enforced; stricter costs more |
| primary, replica | the server that takes writes; the servers that copy it and serve reads |
| `NULL` | "no value". It is not zero and not an empty string, and it behaves strangely in comparisons |

PostgreSQL is the reference database of the week; the behaviour described is its own. The labs use SQLite because it needs no installation.

## Day 1: MVCC and isolation levels

Folder: `d1-mvcc`. Exercise: `w15d1_mvcc.py`.

### Many versions of each row

Two users touch the same row at the same time. The old solution was locks: a reader blocks writers and the reverse. Modern databases use **MVCC**, multi-version concurrency control: a row is **never overwritten**. An update writes a **new version**, stamped with the transaction that created it. Old versions stay for a while.

Each reader has a **snapshot**: the set of transactions that had **committed at the moment the snapshot was taken**. A reader sees, for each row, the newest version created by a transaction in its snapshot, and ignores everything else. **Readers never block writers, and writers never block readers.**

```
key "stock":   version by txn 5: 10      version by txn 9: 7      version by txn 12: 6 (not committed yet)
a reader whose snapshot contains {5, 9} sees 7
a reader whose snapshot contains {5} sees 10
nobody else sees 6 until txn 12 commits
```

A snapshot is fixed when it is taken. A transaction that commits **afterwards** must stay invisible to it, even though it is now committed. Checking only "is that transaction committed now?" lets later commits leak into an older snapshot: the reader sees the data change under its feet in the middle of its work. That is today's review bug.

A transaction always sees its **own** writes.

### Isolation levels

The level decides **when the snapshot is taken** and **what is checked when writing**.

| Level | Snapshot | Prevents | Still possible |
|---|---|---|---|
| **read committed** (PostgreSQL's default) | a new one for each statement | reading uncommitted data | lost updates, write skew |
| **snapshot** (PostgreSQL calls it "repeatable read") | one for the whole transaction | + lost updates | write skew |
| **serializable** | one for the transaction, plus tracking of what was read | everything: the result is the same as running the transactions one after another | nothing; more retries |

### Two anomalies to know by heart

**Lost update.** Two transactions read a counter, 10. Each adds 1 and writes 11. Two increments, one counted. Under snapshot isolation the database applies **first committer wins**: when the second transaction commits, the row it wrote has been changed by a transaction that was not in its snapshot. It gets a **serialization failure** and must be **retried from the start**. Application code at this level needs a retry loop.

**Write skew.** Two doctors are on call. The rule: at least one must stay on call. Each one's transaction checks "is someone else on call?", sees yes, and removes **itself**. They wrote **different rows**, so first-committer-wins sees no conflict. Both commit, and nobody is on call. The rule spanned several rows, and each transaction decided from a snapshot the other was about to invalidate. Only **serializable** catches it (or an explicit lock on the rows that were read).

In a design discussion: say which level you rely on and which of these two anomalies it leaves open.

### Vacuum

Old versions that no snapshot can still see are garbage. A background process (**VACUUM** in PostgreSQL) removes them. It can only remove versions older than the **oldest snapshot still open**. One forgotten transaction left open for a day holds everything back, and tables swell (**bloat**). "Why is the table 40 GB for 2 GB of data?" has this answer more often than any other.

### Traps of the day

- Later commits visible to an older snapshot.
- A transaction that cannot see its own writes.
- First-committer-wins applied at read committed, or missing at snapshot.
- Vacuum removing a version some open snapshot still needs.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `MVCCStore.begin` | start a transaction at a level; take its snapshot | isolation levels |
| `read` | the newest version visible to the snapshot | many versions of each row |
| `write`, `commit`, `abort` | new versions; first committer wins; cancel | two anomalies |
| `vacuum` | remove versions no snapshot can see | vacuum |

Run: `uv run pytest weeks/w15-databases/d1-mvcc -k "not review"`

---

## Day 2: B+tree and index choice

Folder: `d2-btree-indexes`. Exercise: `w15d2_btree.py`.

### Why an index

Without an index, finding the rows where `user_id = 42` means reading every row: a **full scan**, O(n). An index is a sorted structure on that column that reaches them in a few steps.

### The B+tree

The default index of every relational database.

- A tree whose nodes are **pages** of a fixed size (8 KB). Each node holds **many** keys: hundreds. That is the **fan-out**.
- **Internal nodes** hold only separator keys and pointers to children: they are signposts.
- **All the values are in the leaves.**
- The leaves are **linked** from left to right.
- The tree is **balanced**: every leaf is at the same depth, always.

```
                [ 30 | 60 ]                       internal node: keys < 30 go left, 30 ≤ k < 60 middle, ≥ 60 right
              /      |      \
   [5 12 21] → [30 41 55] → [60 72 88]            leaves, linked left to right
```

**Lookup**: from the root, at each node pick the child whose range contains the key, down to a leaf. With a fan-out of several hundred, three or four pages reach any row among a billion. That is why an indexed lookup feels instant at any size.

**Range scan** (`BETWEEN 20 AND 70`, or `ORDER BY`): find the leaf of the first key, then **follow the links** from leaf to leaf until past the last key. A scan that stops at the end of its first leaf silently returns part of the answer. That is today's review bug. It is hard to see in tests with a handful of keys, because everything fits in one leaf.

**Insert**: put the key in its leaf. If the leaf now holds more than the maximum, **split** it into two halves and push a separator key up into the parent. The parent may overflow and split too, up to the root. When the root splits, a new root is created and the tree gains one level. Growth happens at the **top**, which is why all leaves stay at the same depth.

### B-tree against LSM

| | B-tree (PostgreSQL, MySQL) | LSM tree (RocksDB, Cassandra; week 4) |
|---|---|---|
| writes | change pages in place: random writes | appends only: fast |
| reads | one path from root to leaf: fast, predictable | may check several files |
| space | some empty room in pages | several versions until compaction |

### Composite indexes: the leftmost-prefix rule

An index on `(a, b, c)` is sorted by `a`, then by `b` within equal `a`, then by `c`: like a phone book sorted by surname, then first name. It can narrow a search only through a **leftmost prefix** of its columns:

| Query | Uses the index for |
|---|---|
| `a = 1` | `a` |
| `a = 1 AND b = 2` | `a`, `b` |
| `a = 1 AND b > 5` | `a`, then a range on `b` |
| `a = 1 AND b > 5 AND c = 3` | `a` and the range on `b`; **`c` cannot narrow the scan** |
| `b = 2` | nothing: `a` is not fixed |

After the first **range** column, the remaining columns no longer help: inside a range of `b`, the values of `c` are not in order.

The rule of thumb for column order: **equality columns first, then the range or sort column.**

### Covering indexes

An index normally gives the location of a row, and the database then fetches the row from the table. If the index already contains **every column the query needs** (in its key, or added with `INCLUDE`), the table is never touched: an **index-only scan**. For a hot query it is often the largest single speed-up available.

### Traps of the day

- A range scan confined to one leaf.
- A split that loses a key or puts the wrong separator in the parent.
- Leaves not linked after a split.
- A range column placed before an equality column.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `BPlusTree.search`, `insert`, `height` | lookup; insert with splits; number of levels | the B+tree |
| `range` | all keys between two bounds, across leaves | the B+tree |
| `usable_prefix` | how many leading columns of an index narrow a query | composite indexes |
| `is_covering` | can the query be answered from the index alone? | covering indexes |

Run: `uv run pytest weeks/w15-databases/d2-btree-indexes -k "not review"`

---

## Day 3: SQL under pressure

Folder: `d3-sql`. Exercise: `w15d3_sql.py`. Also in the folder: `schema.py`.

Many data-heavy companies put a schema in front of you and ask for queries, live. Six patterns cover nearly everything. The examples below use a small table of their own, so that the exercise stays yours to write. Every one runs:

```python
import sqlite3
db = sqlite3.connect(":memory:")
db.executescript("""
CREATE TABLE sales (id INTEGER PRIMARY KEY, shop TEXT, day TEXT, amount INTEGER);
INSERT INTO sales VALUES (1,'A','d1',10),(2,'A','d2',30),(3,'A','d3',20),(4,'B','d1',5),(5,'B','d2',50);
CREATE TABLE shops (name TEXT, manager TEXT);
INSERT INTO shops VALUES ('A','ann'),('B',NULL),('C','cy');
""")
def q(sql): return db.execute(sql).fetchall()
```

### The order in which a query is evaluated

Not the order in which it is written:

```
FROM / JOIN → WHERE → GROUP BY → HAVING → window functions → SELECT → DISTINCT → ORDER BY → LIMIT
```

Two consequences: a window function cannot be filtered in `WHERE` (it has not been computed yet), so you compute it in a sub-query and filter outside; and `WHERE` runs before `GROUP BY` while `HAVING` runs after.

### Joins

`INNER JOIN` keeps only the rows that match on both sides. `LEFT JOIN` keeps **every row of the left table**; where nothing matches on the right, the right-hand columns are `NULL`.

To keep rows of the left table that have no match (a shop with no sales must still appear, with a total of 0), a condition on the **right** table goes in the `ON` clause. Put in `WHERE`, it removes the `NULL` rows and silently turns the left join into an inner join.

```python
q("SELECT s.name, COALESCE(SUM(x.amount), 0) FROM shops s LEFT JOIN sales x ON x.shop = s.name AND x.amount > 15 GROUP BY s.name ORDER BY s.name")
# [('A', 50), ('B', 50), ('C', 0)]: shop C is still there
```

`COALESCE(a, b)` returns `a`, or `b` when `a` is `NULL`.

### Common table expressions

`WITH name AS (SELECT …) SELECT … FROM name` gives a name to a sub-query. It is how you build a query in readable steps, and how you filter on a window function.

### Window functions

A window function computes a value for **each row**, looking at a group of related rows, **without collapsing them** the way `GROUP BY` does.

```
function(...) OVER ( PARTITION BY the group  ORDER BY the order inside the group )
```

| Pattern | Tool |
|---|---|
| the top N of each group | `ROW_NUMBER() OVER (PARTITION BY … ORDER BY …)` in a CTE, then `WHERE rn <= N` |
| running total | `SUM(x) OVER (PARTITION BY … ORDER BY …)` |
| compare with the previous row | `LAG(x) OVER (PARTITION BY … ORDER BY …)` |

```python
q("""WITH r AS (SELECT shop, day, amount, ROW_NUMBER() OVER (PARTITION BY shop ORDER BY amount DESC, id) AS rn FROM sales)
     SELECT shop, day, amount FROM r WHERE rn = 1 ORDER BY shop""")
# [('A', 'd2', 30), ('B', 'd2', 50)]: the best day of each shop
q("SELECT shop, day, SUM(amount) OVER (PARTITION BY shop ORDER BY day) FROM sales ORDER BY shop, day")
# [('A','d1',10), ('A','d2',40), ('A','d3',60), ('B','d1',5), ('B','d2',55)]: running totals
q("SELECT shop, day, amount - LAG(amount) OVER (PARTITION BY shop ORDER BY day) FROM sales ORDER BY shop, day")
# the change from the previous day; None on the first day of each shop
```

Add a tie-break to every `ORDER BY` inside a window (here `id`), or two equal rows come out in an order that changes from run to run.

### Sessions and "islands"

"Group consecutive events into sessions: a new session starts when the gap since the previous event is larger than a limit." Two steps: with `LAG`, flag each row that **starts** a new group (1 or 0); then take a **running sum of the flags**: it increases by one at each start, so it is a group number.

### Conditional aggregates

Count or sum only some rows inside one pass: `SUM(CASE WHEN condition THEN 1 ELSE 0 END)`.

### Rows with no match, and the `NULL` trap

"Shops that have no sale", an **anti-join**: `NOT EXISTS (SELECT 1 FROM … WHERE it matches)`, or a `LEFT JOIN` followed by `WHERE right.id IS NULL`.

**Never `NOT IN` on a column that can contain `NULL`.** A comparison with `NULL` is neither true nor false: it is **unknown**. `x NOT IN (1, NULL)` means `x <> 1 AND x <> NULL`; the second part is unknown, so the whole condition is never true, and the query returns **no rows at all**, without an error.

```python
q("SELECT 'kept' WHERE 'zed' NOT IN (SELECT manager FROM shops)")                                 # []: one NULL manager empties the result
q("SELECT 'kept' WHERE NOT EXISTS (SELECT 1 FROM shops WHERE manager = 'zed')")                   # [('kept',)]
```

That is today's review bug, and the most common silent error in production SQL. `NULL` is tested with `IS NULL`, never with `= NULL`.

### Reading the plan

`EXPLAIN QUERY PLAN` in front of a query shows how the database will run it. `SCAN` means it reads everything; `SEARCH … USING INDEX` means it uses an index. Tuesday's rule decides the index: equality column first, then the range or sort column.

```python
db.execute("CREATE INDEX sales_shop_day ON sales(shop, day)")
q("EXPLAIN QUERY PLAN SELECT * FROM sales WHERE shop = 'A' AND day >= 'd2'")[0][-1]     # 'SEARCH sales USING INDEX sales_shop_day (shop=? AND day>?)'
```

### Traps of the day

- `NOT IN` with a nullable column.
- A filter on the right table of a `LEFT JOIN` placed in `WHERE`.
- A window function filtered in `WHERE`.
- No tie-break in an `ORDER BY`.

### Today's build

Six functions in `w15d3_sql.py`, each returning **one SQL string**, run on the schema in `schema.py` (provided; read it first). The docstrings give the exact columns and order.

| Function | Pattern | Lesson section |
|---|---|---|
| `revenue_per_country` | left join with a conditional aggregate | joins; conditional aggregates |
| `top2_orders_per_user` | top N per group | window functions |
| `running_revenue` | running total | window functions |
| `users_without_paid_order` | anti-join | rows with no match |
| `sessions_per_user` | sessions | sessions and islands |
| `recent_orders_index_and_query` | a query and the index that serves it | reading the plan |

Run: `uv run pytest weeks/w15-databases/d3-sql -k "not review"`

---

## Day 4: Replication, as the application sees it

Folder: `d4-replication-app-side`. Exercise: `w15d4_replication.py`.

### One primary, several replicas

The **primary** takes all the writes and sends its log of changes to the **replicas**, which apply it and serve reads. Every write has a position in that log, its **LSN** (log sequence number). A replica has applied the log up to some LSN; how far it is behind the primary is its **replication lag**.

| Mode | The primary acknowledges a write… | Cost |
|---|---|---|
| **asynchronous** (the default) | at once, before any replica has it | fast; replicas are behind; a failover loses the writes not yet shipped |
| **synchronous** | once at least one replica has it | no loss if one node dies; every write pays a network round trip |

With a single synchronous replica, its failure blocks all writes. The usual setting is "any one of two".

### What users see when reads go to replicas

Reading from replicas spreads the read load. It also shows users data from the past, in three recognisable ways:

| Anomaly | What the user sees | Fix |
|---|---|---|
| no **read-your-writes** | you post a comment, reload, and it is gone | remember the LSN of the session's last write; read only from a replica **at or past** it, else from the primary |
| non-**monotonic reads** | reload twice: the comment appears, then disappears | remember the highest LSN the session has **seen**; never read from a replica behind it |
| a **stale decision** | stock is checked on a replica, then an order is written | a read that guards a write goes to the primary, inside the write's transaction |

The fix for the first two is **session-aware routing**. The session carries two numbers (in a cookie or a token): the LSN of its last write and the highest LSN it has read at. A replica may serve the session only if it has applied at least both.

Choosing a replica because it is **healthy** is not enough: a healthy replica can be five seconds behind. Routing by health alone gives exactly the disappearing comment. That is today's review bug. Health says "this server answers"; the LSN says "this server knows what this user knows".

### Failover

The primary dies. The most advanced replica is **promoted**. Two dangers:

- **Lost writes**: with asynchronous replication, what the old primary had acknowledged and not yet shipped is gone.
- **Split brain**: the old primary was not dead, only unreachable. It comes back and still believes it is the primary. Two servers now accept writes. The old one must be **fenced**: cut off so that it cannot accept anything (week 3, day 5).

After a failover a session's remembered LSN may be ahead of anything the new primary has: its last writes were among the lost ones. The application must decide what to tell that user.

### Traps of the day

- Replicas chosen by health only.
- The session's "seen" LSN not updated after a read.
- A decision that guards a write made from a replica.
- A promoted replica that is not the most advanced one.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Cluster.write` | write on the primary; update the session | one primary, several replicas |
| `replicate` | a replica applies the log up to an LSN | one primary, several replicas |
| `read` | pick a replica that satisfies the session, or the primary | what users see |
| `failover` | promote the most advanced replica; what is lost | failover |

Run: `uv run pytest weeks/w15-databases/d4-replication-app-side -k "not review"`

---

## Day 5: Money

Folder: `d5-money`. Exercise: `w15d5_money.py`.

"Design a wallet" and "design ticket booking" are asked constantly because they punish sloppiness: a lost update is a lost euro. Five rules carry every such design.

### Rule 1: integers, never floats

```python
0.1 + 0.2 == 0.3, 0.1 + 0.2             # (False, 0.30000000000000004)
10 + 20 == 30                           # True: the same amounts in cents
```

A float cannot represent most decimal fractions exactly. The errors are tiny and they add up across millions of operations, until the books do not balance and nobody can say where the cent went. Store amounts as **integers in the smallest unit** (cents). Amounts as floats is today's review bug.

### Rule 2: a double-entry ledger

Never update a balance in place. `UPDATE accounts SET balance = balance − 50` destroys the history: afterwards nobody can say why the balance is what it is.

Instead every movement is recorded as a set of **entries** that **sums to zero**: a transfer of 50 from A to B is `−50` on A and `+50` on B, written together, atomically, and **never modified afterwards**.

- A **balance** is derived: the sum of an account's entries.
- A **correction** is a new pair of entries in the other direction (a reversal), never an edit.
- The sum of **all** entries of the ledger is always zero. That check, the **trial balance**, is run constantly; the day it is not zero, money was created or destroyed by a bug.

The history then explains every number, which is what auditors, support and your own debugging need.

### Rule 3: idempotency keys

A payment request times out. The client retries. Without protection, the customer is charged twice. The client sends a unique key per **intended operation** (week 2, day 3): the same key again returns the first result and changes nothing; the same key with different parameters is an error. A refused transfer (not enough funds) writes nothing.

### Rule 4: holds with expiry

For scarce things (seats, stock, a card authorisation) a purchase takes two steps: **hold** the item for a few minutes, then **confirm**, or let the hold **expire** and the item returns to sale. Without the hold, two customers pay for the same seat. Without the expiry, an abandoned basket blocks the seat forever.

Expiry compares a time with "now". That "now" must come from **one clock**: the database's. Application servers disagree by seconds (week 3), and with their clocks a hold can be expired for one server and valid for another. In the lab, `now` is always passed in.

### Rule 5: reconcile

Your ledger and the outside world (the bank, the payment provider) drift apart: a notification that never arrived, a refund made by hand in the provider's dashboard. Every day, compare the two lists, payment by payment. Three kinds of difference: a payment only they have; a payment only you have; the same payment with different amounts. Each one is an incident until it is explained.

### Traps of the day

- Amounts as floats.
- A balance stored and updated in place.
- A transfer whose two entries can be written separately.
- A hold checked against the application server's clock.
- A reconciliation that reports a count of differences, not the list.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Ledger.transfer` | two entries that sum to zero, once per idempotency key | rules 1–3 |
| `Ledger.balance`, `trial_balance` | derived balances; the zero check | rule 2 |
| `SeatHolds.hold`, `confirm` | hold with expiry, then sell | rule 4 |
| `reconcile` | the three lists of differences | rule 5 |

Run: `uv run pytest weeks/w15-databases/d5-money -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** redo one drill you marked slow in `PROGRESS.md`, from a blank file, timer on, AI fully off.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 15 when you can do these without notes:

- [ ] explain MVCC and what a snapshot sees
- [ ] give the three isolation levels, and explain lost update and write skew with an example each
- [ ] draw a B+tree, explain a split and a range scan
- [ ] state the leftmost-prefix rule and the rule for column order; say what a covering index is
- [ ] write top-N per group, a running total, an anti-join and a sessions query
- [ ] explain why `NOT IN` with a `NULL` returns nothing
- [ ] explain read-your-writes and monotonic reads, and the routing that provides them
- [ ] give the five rules for handling money

## Optional depth (not needed for the labs)

- Interview questions with short answers: `knowledge/19-databases.md`
- What comes next: `ROADMAP.md`
- Previous week: [`../w14-kubernetes/README.md`](../w14-kubernetes/README.md) · Back to the list: [`../README.md`](../README.md)
