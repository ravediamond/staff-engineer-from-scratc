# Week 5: The system design method

**Everything you need for this week is on this page.** You need weeks 1–4: this week assembles their pieces (heaps, idempotency, fencing, caches) into whole systems. Nothing from other folders is required.

A staff system design round is not about knowing more boxes. It is about running 45 minutes the way you would run a real design review: clarify what matters, put numbers on it, choose a simple design, go deep where the risk is, and say what you would not build. This week installs that method and the estimation reflex on four classic problems, each with a small runnable core you can defend line by line. Friday is the first timed written design.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [The 45-minute frame](#the-45-minute-frame).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-back-of-the-envelope-estimation), [Day 2](#day-2-ids-short-codes-cursor-pagination), [Day 3](#day-3-news-feed), [Day 4](#day-4-chat-ordering-receipts-presence), [Day 5](#day-5-job-scheduler-then-the-first-timed-design).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w5dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w5dN_*.py` | tests | run, never edit |
| `review_w5dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

Friday's folder also has `design.md` (the prompt), and `rubric.md` (how to grade yourself). You write your answer in a new file, `my_design.md`.

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w5-design-method/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w5-design-method/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w5-design-method/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w5-design-method/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | You learn | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-estimation` | orders of magnitude, fast | QPS, storage, bandwidth, GPU count, cost | a unit |
| Tue | `d2-ids-pagination` | identifiers and paging at scale | base62, Snowflake IDs, cursor pagination | fields that overlap |
| Wed | `d3-news-feed` | push against pull | a feed service with a hybrid fan-out | a sort order |
| Thu | `d4-chat-presence` | ordering, duplicates, receipts, presence | a chat service and a presence tracker | a pointer that moves the wrong way |
| Fri | `d5-job-scheduler` | leases, retries, dead letters; then the first timed design | a job queue | who may complete a job |

## The 45-minute frame

Memorise it. Every Friday design from now on uses it, and so will every real interview.

| Min | Phase | What a staff candidate does |
|---|---|---|
| 0–5 | Requirements | 3–5 functional requirements; non-functional ones **with numbers** (requests per second, p99 latency, durability, consistency); **explicit non-goals** |
| 5–10 | Estimation | users → requests per second (average and peak) → storage per year → bandwidth → cost or GPUs. One line each, rounded |
| 10–15 | API and data model | the 3–5 calls; the 2–4 tables or records; how they are read and written |
| 15–25 | High-level design | the simplest design that meets the numbers; walk one request from end to end |
| 25–40 | Two deep dives | **you** pick the two riskiest parts (a hot key, consistency, a failure, cost) and discuss trade-offs with numbers |
| 40–45 | Wrap-up | bottlenecks, what you would monitor, what you would build next, what you chose not to build |

What separates levels: a senior candidate produces a correct design. A staff candidate drives the conversation, states assumptions and non-goals without being asked, sizes things before drawing them, chooses the deep dives, and names what could go wrong and how they would know.

Words used all week: **QPS**, queries (requests) per second. **DAU**, daily active users. **p99**, the latency that 99% of requests beat. **Fan-out**, one event that causes many writes or reads. **Hot key**, one key that receives a large share of the traffic.

## Day 1: Back-of-the-envelope estimation

Folder: `d1-estimation`. Exercise: `w5d1_estimation.py`.

### What estimation is for

Not precision. An **order of magnitude, fast, with the assumptions said out loud**, so that the design fits the load. "About 12 000 requests per second at peak" decides between one machine and a fleet. Being wrong by 30% changes nothing; being wrong by 100 times changes everything.

### Five conversions

| From | To | Rule |
|---|---|---|
| daily users × actions per day | average QPS | divide by 86 400 seconds per day (about 10⁵) |
| average QPS | peak QPS | multiply by 2 to 10; **say your factor** |
| items per day × bytes × days × copies | storage | 1 KB × 1 million per day ≈ 1 GB per day ≈ 365 GB per year |
| QPS × bytes per request | bandwidth | **multiply by 8 for bits**: networks are measured in bits per second |
| seconds of GPU work arriving per second | GPUs | round **up**, then add headroom |

A worked line: 10 million daily users, 20 actions each → 200 million per day → about 2 300 per second on average → about 7 000 at peak with a factor of 3.

Numbers worth knowing: a day has 86 400 seconds; a year about 31.5 million. 1 KB = 10³ bytes, MB 10⁶, GB 10⁹, TB 10¹², PB 10¹⁵ (decimal units, the ones used here).

Bits against bytes is the classic slip, and today's review bug: 100 MB per second is 800 megabits per second.

### Estimating LLM serving

A model reads its input and then writes its output one token at a time. A GPU has two throughputs, both measured, never guessed:

- **prefill**: input tokens processed per second. Fast.
- **decode**: output tokens produced per second, summed over all the requests it is serving together. Slower.

One request costs `input tokens / prefill rate + output tokens / decode rate` seconds of GPU. So:

```
GPUs ≈ peak QPS × ( input tokens / prefill rate + output tokens / decode rate ) × headroom       rounded up
```

Monthly cost: GPUs × price per GPU-hour × hours in the month × the fraction of time they are rented.

### A floating-point detail

`30 * (0.1 + 0.2)` is `9.000000000000002` in a computer, and rounding that up gives 10 instead of 9. Round to a few decimals before rounding up:

```python
import math
math.ceil(30 * (0.1 + 0.2)), math.ceil(round(30 * (0.1 + 0.2), 9))     # (10, 9)
```

### Traps of the day

- Bytes reported as bits, or the reverse.
- A peak with no stated factor.
- Replication forgotten in storage.
- GPUs rounded to the nearest instead of up.

### Today's build

| Function | Job | Lesson section |
|---|---|---|
| `qps` | average and peak | five conversions |
| `storage_bytes` | total after some years, copies included | five conversions |
| `bandwidth_gbps` | gigabits per second | five conversions |
| `llm_gpus` | GPUs for a peak load | estimating LLM serving |
| `monthly_cost` | cost of the provisioned GPUs | estimating LLM serving |
| `human_bytes` | `'1.5 KB'`, `'40.0 TB'` | numbers worth knowing |

Run: `uv run pytest weeks/w5-design-method/d1-estimation -k "not review"`

---

## Day 2: IDs, short codes, cursor pagination

Folder: `d2-ids-pagination`. Exercise: `w5d2_ids.py`.

### Identifiers at scale

Every record needs a unique id. The options:

| Kind | Problem |
|---|---|
| a counter in one database (auto-increment) | one machine must hand out every id: a bottleneck and a single point of failure; ids reveal your volume |
| a random UUID | 128 bits; random order, so new rows land all over the index |
| **Snowflake-style** (Twitter, Discord) | 64 bits, roughly ordered by time, generated on any machine with no coordination |

A Snowflake id packs three numbers into one 64-bit integer:

```
| 1 bit: 0 | 41 bits: milliseconds since a chosen start date | 10 bits: worker id | 12 bits: sequence |
```

- 41 bits of milliseconds last about 69 years.
- 10 bits: 1 024 machines, each with its own worker id.
- 12 bits: up to 4 096 ids per millisecond per machine.

**Packing with bit operations.** `x << n` shifts `x` left by `n` bits (multiplies by `2ⁿ`); `|` combines fields that do not overlap; `>>` and `&` take them apart.

```python
packed = (5 << 12) | 7                       # a 5 placed above 12 bits, then a 7 in the low 12 bits
packed >> 12, packed & ((1 << 12) - 1)       # (5, 7): unpacked
```

Each field must be shifted by the total width of the fields to its right. A wrong shift makes two fields overlap and produces duplicate ids. That is today's review bug.

Three rules of the generator: within the same millisecond, increase the sequence; if the sequence overflows, wait for the next millisecond; if the clock moves **backwards**, **refuse**. An id built from a time already used can repeat an old id.

### Short codes

A URL shortener shows an integer id in a compact alphabet: digits, lower-case and upper-case letters, 62 characters. That is **base 62**. Seven characters give `62⁷ ≈ 3.5 × 10¹²` codes. Encoding is repeated division by 62, reading the remainders; decoding is the reverse. Zero needs its own case.

### Pagination

**Offset pagination**, `OFFSET 10000 LIMIT 20`, has two faults. The database walks and discards 10 000 rows to return 20. And under writes it is wrong: if a new row is inserted at the top between two page requests, every row shifts down by one and the next page repeats an item.

**Cursor pagination** (also called keyset): the client sends back a **cursor** that encodes the sort key of the last item it received, and the server returns "the items strictly **after** this key". Cost independent of the depth, and stable under inserts.

Two requirements. The sort key must be **unique**: with "newest first" and two items created in the same millisecond, add the id as a tie-break, so the order is `(created_at descending, id descending)`. And the cursor should be **opaque** to clients, so they do not depend on its content: JSON, encoded in URL-safe base64.

```python
import base64, json
cur = base64.urlsafe_b64encode(json.dumps({"c": 1700, "i": 42}).encode()).decode()
json.loads(base64.urlsafe_b64decode(cur))        # {'c': 1700, 'i': 42}
```

Python compares tuples element by element, which makes "strictly after `(created_at, id)`" one comparison.

### Traps of the day

- Fields of an id that overlap.
- A generator that keeps going when the clock went back.
- A cursor on a key that is not unique: items skipped or repeated at the page border.
- "After the cursor" with `<=`: the last item of a page appears again.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `base62_encode`, `base62_decode` | integer ↔ short code | short codes |
| `Snowflake.next_id`, `snowflake_decode` | pack and unpack; the three rules | identifiers at scale |
| `encode_cursor`, `decode_cursor` | opaque cursors | pagination |
| `paginate` | one page and the next cursor | pagination |

Run: `uv run pytest weeks/w5-design-method/d2-ids-pagination -k "not review"`

---

## Day 3: News feed

Folder: `d3-news-feed`. Exercise: `w5d3_feed.py`.

### The problem

Users follow other users. Each user's feed shows the recent posts of the people they follow, newest first. The design question is **when** the work is done.

| Model | When someone posts | When someone reads | Breaks when |
|---|---|---|---|
| **fan-out on write** (push) | copy the post id into the **inbox** of every follower | read your own inbox: one cheap read | an author has 50 million followers: one post is 50 million writes |
| **fan-out on read** (pull) | write only to the author's own **outbox** | fetch the outbox of everyone you follow and merge | you follow 2 000 accounts: one read is 2 000 fetches |
| **hybrid** | push for ordinary authors | read your inbox, and pull only from the few very popular accounts you follow | needs a threshold and a merge |

Reads are far more frequent than posts, so push is the default: pay at write time and make reads cheap. The hybrid treats the few "celebrity" authors separately because pushing their posts costs too much. This is what large social networks do.

### The merge

A feed read combines several lists, each already sorted newest first: the inbox, the outbox of each followed celebrity, and the user's own posts. Combining sorted lists into one sorted list, truncated to `n`, is week 1's heap problem.

```python
import heapq
a = [(9, "p9"), (5, "p5")]; b = [(8, "p8"), (2, "p2")]          # (timestamp, post), newest first
list(heapq.merge(a, b, reverse=True))[:3]                       # [(9, 'p9'), (8, 'p8'), (5, 'p5')]
```

Newest first means **descending** timestamps at every step: in the inputs, in the merge, in the output. One ascending sort in the middle returns the oldest posts. That is today's review bug.

A post can reach a reader by two paths. The result must not contain it twice.

### Capped inboxes

Nobody scrolls back 10 000 items. An inbox keeps the most recent few hundred entries and drops the rest. It bounds the storage per user.

### Counting the cost

The service counts its `writes` and `reads`, and `fanout_writes` computes how many inbox writes one post from each author causes for a given celebrity threshold. Put those numbers in front of a design discussion: the threshold is a trade between write cost and read cost, and you can plot it.

### Traps of the day

- An ascending sort somewhere.
- A celebrity's posts pushed anyway.
- Duplicates in the merged feed.
- An inbox that grows without limit.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `fanout_writes` | inbox writes for a threshold | counting the cost |
| `FeedService.follow`, `post` | push unless the author is a celebrity; always write the outbox | the problem |
| `FeedService.feed` | inbox + celebrity outboxes + own posts, newest first, no duplicates | the merge |

Run: `uv run pytest weeks/w5-design-method/d3-news-feed -k "not review"`

---

## Day 4: Chat: ordering, receipts, presence

Folder: `d4-chat-presence`. Exercise: `w5d4_chat.py`.

Chat looks simple and hides three problems from weeks 2 and 3.

### Ordering

Phones' clocks are wrong, so messages cannot be ordered by the time the client says. The **server** gives each message a **sequence number**, increasing by one, **per conversation**. Everyone displays a conversation in the order of `seq`.

Per conversation, not global. A single global order over all conversations would need one writer for the whole system, and nobody needs to know whether a message in one chat came before a message in another. Do not pay for an order nobody uses; say that sentence in the interview.

### Duplicates

A phone on a bad network sends a message, gets no answer, and sends it again. Each message carries an id chosen by the client, `client_msg_id`. If the server has already seen that id in that conversation, it returns the sequence number it gave the first time and stores nothing new. It is the idempotency key of week 2.

### Read receipts

"Read up to message N" is one number per user and per conversation: a **pointer**. Acknowledgements arrive out of order on a flaky network: "read up to 12" can arrive after "read up to 15". So the update is

```
read[user, conversation] = max( current value, N )
```

The pointer only ever moves **forward**. Without the `max`, a late message moves it back and the unread badge reappears on messages already read. That is today's review bug. The number of unread messages is the latest sequence number minus the pointer.

### Presence

"Is this user online?" Clients send a **heartbeat** every 30 seconds or so. A user is online if their last heartbeat is more recent than a timeout of about two heartbeats.

Never store `online = true` and wait for an "offline" message to clear it. A phone that loses its battery or its network never sends "offline", and the user stays online forever. With a timestamp and a timeout, a silent client goes offline by itself.

### Traps of the day

- One sequence for all conversations.
- A retried message stored twice.
- A read pointer assigned without `max`.
- Presence as a flag.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `ChatService.send` | assign `seq`; deduplicate by `client_msg_id` | ordering; duplicates |
| `fetch` | messages after a given `seq`, limited | ordering |
| `mark_read`, `unread` | the forward-only pointer | read receipts |
| `Presence` | `heartbeat`, `is_online`, `online` | presence |

Run: `uv run pytest weeks/w5-design-method/d4-chat-presence -k "not review"`

---

## Day 5: Job scheduler, then the first timed design

Folder: `d5-job-scheduler`. Exercise: `w5d5_jobs.py`. Also in the folder: `design.md`, `rubric.md`.

### The lab: a job queue

Every ML platform has one: evaluation runs, batch inference, embedding backfills, fine-tuning jobs. Its core is the same as Amazon SQS or Celery.

**Lease.** A worker does not take a job forever. It takes it for `lease_seconds`. If it has not reported completion by then, it has probably died, and the job becomes available to others. (Queues call this the visibility timeout.)

**Lease token.** A slow worker is not a dead worker. Worker A takes a job; its lease expires; worker B takes the same job; then A finishes and reports "done". Without a check, A completes a job that B is still running. So every lease comes with a fresh **token**, and `complete` and `fail` are accepted only with the token of the **current** lease. It is the fencing token of week 3.

**Retries and the dead-letter queue.** A job that fails, or whose lease expires, goes back in the queue and its attempt count goes up. After `max_attempts` it is moved to the **dead-letter queue (DLQ)**: a place where a human looks at it. Without it, a job that always crashes its worker (a **poison** job) circulates forever and eats capacity.

**Order.** Higher priority first; within a priority, first in, first out; a job with a `run_at` in the future is not available before that time. A heap of tuples gives this order; a counter that increases with each submission breaks ties in arrival order.

**Reaping** is finding the leases that have expired and re-queuing their jobs, with the injected clock.

### Traps of the day

- `complete` accepted with an old token.
- An expired lease that does not count as an attempt: a poison job never reaches the DLQ.
- A delayed job handed out early.
- FIFO lost inside a priority.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `JobQueue.submit` | priority, optional `run_at` | order |
| `lease` | the next available job and a fresh token | lease; lease token |
| `complete`, `fail` | only with the current token | lease token; retries |
| `reap` | expire leases | reaping |
| `dlq`, `state` | where jobs end up | the dead-letter queue |

### After the lab: the Friday design (45 minutes, timed)

1. Open `design.md` and read the prompt.
2. Start a 45-minute timer. Write your design in `my_design.md`, following [the 45-minute frame](#the-45-minute-frame). Stop when the timer rings, even in the middle of a sentence.
3. Grade yourself with `rubric.md`: for each line, the level your answer signals.
4. Only then, read the model answer: `model_answer.md`, in the same folder on the `solutions` branch.
5. Write in `PROGRESS.md` the one thing that would have raised your level.

No one, and no AI, writes `my_design.md` for you. Ask for a graded review after it is written.

Run: `uv run pytest weeks/w5-design-method/d5-job-scheduler -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w05`, timer on, AI fully off: `uv run pytest drills/w05 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 5 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 5 when you can do these without notes:

- [ ] recite the 45-minute frame with its timings
- [ ] go from daily users to peak QPS, storage per year, bandwidth and GPUs in two minutes, out loud
- [ ] draw the bit layout of a Snowflake id and state its three rules
- [ ] explain why offset pagination is slow and wrong, and how a cursor fixes both
- [ ] compare fan-out on write and on read, and say when the hybrid is needed
- [ ] explain per-conversation sequence numbers, forward-only read pointers and heartbeat presence
- [ ] explain leases, lease tokens and the dead-letter queue

## Optional depth (not needed for the labs)

- The method at length, the numbers to know, and questions with answers: `knowledge/05-design-method-and-estimation.md`
- How each level is judged, line by line: `knowledge/12-staff-rubrics.md`
- Previous week: [`../w4-storage-retrieval/README.md`](../w4-storage-retrieval/README.md) · Next: [`../w6-rag/README.md`](../w6-rag/README.md)
