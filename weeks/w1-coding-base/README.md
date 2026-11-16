# Week 1: Coding base and communication

**Everything you need for this week is on this page.** You need Python and `uv sync` done once at the repo root. Nothing from other folders is required.

Staff loops at Google and Meta still have two coding rounds. They are not easier at staff level; the bar moves from "solved it" to "solved it cleanly, said the invariant, tested it, talked like someone I want next to me in an incident". This week rebuilds, from scratch, the five structures that sit inside half of all interview problems.

## Start here

1. Read [The week in one table](#the-week-in-one-table) and [Three ideas used every day](#three-ideas-used-every-day).
2. Each day, open that day's folder and follow [What to do each day](#what-to-do-each-day).
3. The lesson for each day is the matching section of this page: [Day 1](#day-1-binary-heap-heapify-top-k), [Day 2](#day-2-open-addressing-hash-map), [Day 3](#day-3-lru-and-ttl-caches), [Day 4](#day-4-trie-and-autocomplete), [Day 5](#day-5-intervals-booking-sweep-line).
4. Friday: [End of the week](#end-of-the-week).

### What is in a day folder

| File | What it is | You |
|---|---|---|
| `predict.md` | small questions, answered before you read anything | write guesses |
| `README.md` | one-page summary of the day, with its "staff angle" | read after the lesson |
| `predict_run.py` | prints the real answers | run, compare |
| `w1dN_*.py` | **the exercise**, with `# TODO` | **write the code** |
| `test_w1dN_*.py` | tests | run, never edit |
| `review_w1dN.py` + its test | code with one planted bug | **find and fix**, write the `WHY:` line |
| `questions.md` | interview questions | answer out loud |

### What to do each day

One hour, commands from the repo root.

| Min | Step | Command or file |
|---|---|---|
| 0–5 | Retrieve (Monday: 10-min delayed recall of last week's hardest function instead) | `uv run python scripts/review.py` |
| 5–10 | Guess, before reading | `predict.md` |
| 10–18 | Read the lesson | the day's section on this page |
| 18–20 | Check your guesses | `uv run python weeks/w1-coding-base/<day>/predict_run.py` |
| 20–45 | Build, narrating out loud | `uv run pytest weeks/w1-coding-base/<day> -k "not review"` until green |
| 45–53 | Review | `uv run pytest weeks/w1-coding-base/<day> -k review` |
| 53–60 | Explain | `questions.md` out loud, then `uv run python scripts/review.py add weeks/w1-coding-base/<day>` |

Guess before reading even if you know nothing: a wrong guess makes the lesson stick (`LEARNING.md` rule 1). AI stays off in the exercise files; stuck for 10 minutes, ask for a hint, not code.

## The week in one table

| Day | Folder | You learn | You build | The review bug is about |
|---|---|---|---|---|
| Mon | `d1-heap` | the binary heap; how to talk while coding | a min-heap, heapify, heap sort, top-k | which child a node is compared with |
| Tue | `d2-hash-map` | how a hash map works inside | an open-addressing map with tombstones and resize | what delete leaves behind |
| Wed | `d3-lru-cache` | O(1) caches: map + linked list; expiry | an LRU cache and a TTL cache | what a read does to recency |
| Thu | `d4-trie` | prefix trees | a trie with delete and top-k autocomplete | when a path is a word |
| Fri | `d5-intervals` | sort, then one pass | merge, insert, peak overlap, a booking calendar | the sort key |

## Three ideas used every day

**1. Complexity.** How the cost of an operation grows with the size `n` of the input, ignoring constants.

| Notation | Name | Example | n = 1 000 000 |
|---|---|---|---|
| O(1) | constant | read `a[i]`, look up a key in a dict | 1 step |
| O(log n) | logarithmic | binary search; one heap operation | about 20 steps |
| O(n) | linear | one pass over a list | 1 000 000 |
| O(n log n) | | sorting | about 20 000 000 |
| O(n²) | quadratic | every pair | 10¹²: too slow |

Say the complexity of your approach **before** you write code, for time and for memory.

**2. Invariant.** A statement that is true before and after every operation on a structure. "The smallest item is at index 0." Every operation may break it for a moment and must restore it before returning. If you can say the invariant, you can write the code and you can find the bug: a bug is a place where the invariant stops holding. Every non-trivial function you write in this repo gets a one-line `# invariant:` comment.

**3. Inject what you cannot control.** A function that reads the clock or draws random numbers cannot be tested exactly. So time and randomness are passed in as arguments: `clock` is a function that returns the current time, and a test passes a fake one. You will see `clock`, `sleep` and `rng` parameters all through this course.

```python
class FakeClock:
    def __init__(self): self.t = 0.0
    def __call__(self): return self.t

clock = FakeClock()
clock.t += 30          # the test moves time forward: no waiting, same result on every run
clock()                # 30.0
```

## Day 1: Binary heap, heapify, top-k

Folder: `d1-heap`. Exercise: `w1d1_heap.py`.

### What a heap is for

You have a collection that changes, and you repeatedly need its **smallest** item. A sorted list gives the smallest in O(1) and costs O(n) per insertion. A **heap** gives the smallest in O(1) and costs O(log n) for both insertion and removal. Uses: "the k largest", "merge k sorted lists", schedulers ("the job with the earliest deadline"), Dijkstra.

Python ships one, `heapq`. You may not use it today; it is your reference.

```python
import heapq
h = []
for x in [5, 1, 9, 3]:
    heapq.heappush(h, x)
heapq.heappop(h), h[0]       # (1, 3): the smallest leaves, the next smallest is at index 0
```

### A tree stored in a list

A heap is a binary tree that is filled level by level, left to right, and stored in a plain list. No pointers: positions do the work.

```
index:   0  1  2  3  4  5            tree:        1
value:   1  3  2  7  4  9                       /   \
                                               3     2
children of i: 2i+1 and 2i+2                  / \   /
parent of i:   (i-1)//2                      7   4 9
```

**Invariant (min-heap): every node is smaller than or equal to its children.** So the smallest is at the root, index 0. Nothing is said about left against right: a heap is not sorted.

### Every operation: break in one place, repair along one path

| Operation | What you do | Repair | Cost |
|---|---|---|---|
| push | append at the end | **sift up**: while smaller than its parent, swap with the parent | O(log n) |
| pop | take the root; move the last item to the root; shrink | **sift down**: while larger than a child, swap with the **smaller** child | O(log n) |
| heapify | make a heap from any list, in place | sift down every node that has children, from the last one back to the root | **O(n)** |

The tree has about `log₂ n` levels, so one repair path is short.

**Why the smaller child.** After the swap, the child that moved up becomes the parent of the other child. It must be smaller than or equal to it. Only the smaller of the two guarantees that.

**Why heapify is O(n) and not O(n log n).** Half the nodes are leaves and do no work. A quarter can move down one level, an eighth two levels. The sum `n/4·1 + n/8·2 + n/16·3 + …` stays below `n`. Starting from the **last** internal node, index `n//2 − 1`, means that when you sift a node down, both subtrees below it are already heaps.

A trace of pop on `[1, 3, 2, 7, 4, 9]`: take 1; move 9 to the root → `[9, 3, 2, 7, 4]`; children of 9 are 3 and 2, the smaller is 2, swap → `[2, 3, 9, 7, 4]`; index 2 has no children: done.

### Top-k of a stream

To keep the `k` **largest** items of a stream, keep a **min**-heap of size `k`. Its root is the smallest of your current top `k`: the one to beat. A new item enters only if it is larger than the root, and then the root leaves. Time O(n log k), memory O(k). A max-heap would need all `n` items in memory.

### How to talk while coding

Coding rounds score communication as much as correctness. Say these five things, in this order, out loud, even alone. Use it every day from now on.

1. **Restate and give examples** (1 min): input, output, one worked example, the edge cases (empty, one item, duplicates, `k = 0`, `k > n`).
2. **Approach and complexity, before code** (2 min): the brute force and its cost, the better idea and its cost.
3. **The invariant**, in one sentence.
4. **Code, narrating intent**: "now the repair step", not "now I write a while loop".
5. **Test by hand, then edge cases**: walk one example through your code line by line.

### Traps of the day

- Sift-down comparing with the left child only.
- Sift-down reading a child index that is past the end.
- Heapify from the root downward: the subtrees are not heaps yet.
- A max-heap for top-k largest.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `MinHeap` | `push`, `pop`, `peek`, length, with `_sift_up` and `_sift_down` | every operation |
| `heapify` | in place, bottom-up | every operation; why O(n) |
| `heap_sort` | a new ascending list, using your own heap functions | pop repeatedly gives sorted order |
| `top_k_largest` | size-`k` min-heap, result in descending order | top-k of a stream |

Run: `uv run pytest weeks/w1-coding-base/d1-heap -k "not review"`

---

## Day 2: Open-addressing hash map

Folder: `d2-hash-map`. Exercise: `w1d2_hashmap.py`.

### What a hash map is

A structure that finds a value by its key in O(1) on average. Python's `dict` is one. Inside there is an **array of slots** and a **hash function** that turns a key into a number. `hash(key) % capacity` is the slot where the search for that key starts.

Two different keys can land on the same slot: a **collision**. Two families of answers:

| | Separate chaining | Open addressing (today) |
|---|---|---|
| On a collision | each slot holds a small list; append to it | look at the next slot, then the next (**linear probing**) |
| Memory | scattered | one flat array, friendly to the CPU cache |
| Used by | Java `HashMap` | CPython `dict`, Rust, Go |

### Linear probing, by hand

Capacity 8. Keys A, B, C all hash to slot 2.

```
put A → slot 2 is free            [ . . A . . . . . ]
put B → 2 taken, try 3            [ . . A B . . . . ]
put C → 2, 3 taken, try 4         [ . . A B C . . . ]
get C → start at 2: A? no. 3: B? no. 4: C. found
get D (hashes to 2) → 2, 3, 4 are other keys, 5 is EMPTY → D is absent, stop
```

The search stops at the first **empty** slot. At the end of the array it wraps to index 0.

**Invariant:** if a key is stored at slot `j`, every slot from its home slot up to `j` is occupied. An empty slot on that path would make `get` stop too early.

### Why delete needs a tombstone

Delete B by emptying slot 3: `[ . . A . C . . . ]`. Now `get C` starts at 2, sees A, moves to 3, finds it empty, and reports "absent". C is still in the table and can no longer be found.

So delete writes a special marker, a **tombstone**, meaning "something was here, keep going". `get` walks over tombstones. `put` may reuse the first tombstone it met, but only after checking that the key is not further along the path, or the same key would be stored twice.

### Load factor and resizing

The **load factor** is the fraction of slots that are not empty: `(live + tombstones) / capacity`. Tombstones count: they lengthen searches just like live entries. As the table fills, runs of occupied slots merge and searches get long. For a key that is absent, the expected number of probes is about `½ · (1 + 1/(1 − α)²)`: 2.5 at α = 0.5, 50 at α = 0.9.

So when the load factor passes about 2/3, **resize**: allocate an array twice as large and re-insert every live entry. Positions depend on the capacity, so every key must be placed again; tombstones are simply not copied. A resize costs O(n) but happens rarely enough that the average cost per insertion stays O(1) (**amortised**).

Python's own `hash()` is fine inside one process. Note that for strings it changes from one run of Python to the next.

### Traps of the day

- Delete that empties the slot.
- `put` that stops at the first tombstone and creates a duplicate key.
- No wrap-around at the end of the array.
- Load factor computed without the tombstones: the table fills with tombstones and searches never end.
- A resize that copies slots at the same indices.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `OpenAddressingMap._find` | walk the probe sequence for a key | linear probing; tombstones |
| `put`, `get`, `delete` | `KeyError` when the key is missing | linear probing; tombstones |
| `_resize` | double, re-insert live entries | load factor and resizing |
| `keys`, length, `in` | the live keys | — |

A `probes` counter lets the tests check that you do not scan the whole table.

Run: `uv run pytest weeks/w1-coding-base/d2-hash-map -k "not review"`

---

## Day 3: LRU and TTL caches

Folder: `d3-lru-cache`. Exercise: `w1d3_lru.py`.

### What a cache is, and why it must forget

A cache keeps the results of slow operations in memory so the next request is fast. Memory is limited, so a cache has a **capacity** and, when full, an **eviction policy**: which entry to throw away. **LRU** (least recently used) throws away the entry that has not been touched for the longest time, betting that what was used recently will be used again.

Both operations, `get` and `put`, must be O(1). That needs two structures working together.

### Map plus doubly linked list

- A **hash map** finds an entry by key in O(1). It knows nothing about order.
- A **doubly linked list** keeps the entries in order of recency. Each node knows its previous and its next node, so a node can be removed from the middle in O(1) by connecting its two neighbours to each other.

The map's values are the **nodes** of the list.

```
map:   key → node
list:  HEAD ⇄ n3 ⇄ n1 ⇄ n7 ⇄ TAIL        most recent next to HEAD, least recent next to TAIL
```

`HEAD` and `TAIL` are **sentinels**: two fake nodes that are always there and hold no data. With them, every real node always has a previous and a next node, and the code needs no "is the list empty?" branch.

Two small moves build everything:

```
unlink(node):      node.prev.next = node.next ;  node.next.prev = node.prev
push_front(node):  insert between HEAD and HEAD.next        (four pointers to set)
```

| Operation | Steps |
|---|---|
| `get(key)` | find the node in the map; unlink it; push it to the front; return its value |
| `put(key, value)`, key exists | update the value; move the node to the front |
| `put(key, value)`, new key | new node at the front, add to the map; if over capacity, remove the node before `TAIL` **and its key from the map** |

**Invariant, in two halves:** the map and the list hold exactly the same entries, at most `capacity` of them; and the list order is the order of last use. Every LRU bug breaks one half. A `get` that returns the value without moving the node breaks the second.

To delete from the map at eviction you need the key of the evicted node. So a node stores its key as well as its value.

### Expiry (TTL)

A **time to live** says how long an entry may be served. Each entry stores `expires_at = now + ttl`.

- **Lazy expiry**: check on `get`. If the entry has expired, remove it and answer as if it were absent. Cheap; dead entries that nobody reads stay in memory.
- **Active expiry**: a sweep that removes expired entries. Redis does both: lazy, plus a periodic sampled sweep.

Time comes from an injected `clock` (see "three ideas"). Never call `time.time()` inside code you want to test.

### Traps of the day

- `get` does not refresh recency.
- Eviction removes the node and leaves its key in the map: the map grows without limit.
- An existing key handled as a new one: the size counts it twice.
- Capacity of zero.
- An expired entry returned because expiry is only checked in the sweep.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `LRUCache` | `get`, `put`, length, `keys_mru`; a hand-written list with sentinels, no `OrderedDict` | map plus doubly linked list |
| `TTLCache` | LRU with per-entry expiry, lazy on `get`; `purge_expired` returns the number removed | expiry |

Run: `uv run pytest weeks/w1-coding-base/d3-lru-cache -k "not review"`

---

## Day 4: Trie and autocomplete

Folder: `d4-trie`. Exercise: `w1d4_trie.py`.

### What a trie is

A tree that stores strings **character by character**. Each node has a dict from character to child node. Words that share a prefix share the path for that prefix.

```
insert "car", "cart", "cat"

root ─ c ─ a ─ r*  ─ t*          * marks "a word ends here"
              └ t*
```

Looking up a word costs O(length of the word), whatever the number of words stored. And a trie answers a question a hash map cannot: "which words start with this prefix?".

### A path is not a word

`"ca"` exists as a path above. It was never inserted. So each node carries a flag `is_word`.

**Invariant:** a word is in the set if and only if walking its characters from the root ends on a node whose `is_word` is true. `contains("ca")` is false; `starts_with("ca")` is true. Inserting `"car"` after `"cart"` creates no new node: it only sets a flag, and forgetting to set it is the classic bug.

Today each word also has a `count`: how many times it was inserted. Inserting the same word again adds to its count.

### Delete, with pruning

Deleting a word clears its flag. Nodes that are then useless should be removed, or the trie only ever grows. A node is useless when it is not the end of a word **and** has no children. Walk back from the end of the deleted word toward the root, removing nodes while that holds, and stop at the first node that is still needed.

Delete `"cart"` above: node `t` is useless, remove it. Node `r` is still the end of `"car"`: stop. Deleting a word that is not there returns `False` and changes nothing.

### Top-k autocomplete

"The `k` most frequent words that start with this prefix." Walk to the node of the prefix. Collect every word in the subtree below it, with a depth-first traversal that carries the characters read so far. Then keep the best `k`.

The order is fixed so that results are reproducible: higher count first, and for equal counts, alphabetical order. Sorting with a key that is a tuple does both at once:

```python
words = [("cat", 5), ("car", 5), ("cart", 9)]
sorted(words, key=lambda wc: (-wc[1], wc[0]))     # [('cart', 9), ('car', 5), ('cat', 5)]
```

| Design | Query cost | Memory | Update cost |
|---|---|---|---|
| traverse the subtree at query time (today) | size of the subtree | small | O(length) |
| store the top `k` at every node | O(length + k) | `k` entries per node | O(length · k) |

Real suggestion systems compute the top `k` per prefix offline and serve it from a key-value store. The trie is the mental model.

### Traps of the day

- `contains` true for any existing path.
- A word that is a prefix of another never marked as a word.
- Delete that removes nodes still used by another word.
- Ties in top-k left in arbitrary order.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `Trie.insert` | add a word, accumulate its count | what a trie is; a path is not a word |
| `contains`, `starts_with` | word or prefix | a path is not a word |
| `delete` | clear, prune, `False` if absent | delete, with pruning |
| `top_k` | most frequent words under a prefix | top-k autocomplete |
| `node_count` | used by the tests to check pruning | — |

Run: `uv run pytest weeks/w1-coding-base/d4-trie -k "not review"`

---

## Day 5: Intervals, booking, sweep line

Folder: `d5-intervals`. Exercise: `w1d5_intervals.py`.

### The one move

An interval is a pair `(start, end)`: a meeting, a job, a booking. Almost every interval problem is solved the same way: **sort by start, then one pass with a small amount of state.**

### The convention: half-open

Today intervals are **half-open**, written `[start, end)`: the start is included, the end is not. `[1, 3)` and `[3, 5)` do **not** overlap: a meeting that ends at 3 and one that starts at 3 can share a room. Two intervals `[a, b)` and `[c, d)` overlap exactly when `a < d and c < b`.

Say your convention out loud in an interview. Half of all interval bugs are a `<` that should be `<=`.

### Merge

Sort by start. Keep the interval being built. For each next interval: if it starts at or before the end of the current one, extend the current end (take the **maximum** of the two ends: the next interval may be entirely inside). Otherwise the current one is finished: output it and start a new one.

```
input:   [1,3) [2,6) [8,10) [9,12) [12,13)
sorted by start (already)
[1,3) + [2,6)   → [1,6)        2 ≤ 3: extend
[8,10)          → new          8 > 6
[8,10) + [9,12) → [8,12)
[12,13)         → [8,13)       12 ≤ 12: touching intervals leave no gap, they merge
output:  [1,6) [8,13)
```

**Invariant:** after processing the first `i` intervals in start order, the output is sorted, non-overlapping, and covers exactly their union. Sorting by start is what makes "compare only with the last output interval" correct. Sorted by end, an interval that starts early and ends late arrives after intervals it should have absorbed.

Note the two different questions: touching intervals do not **overlap** (no shared instant), and they do **merge** (no gap between them).

### Insert into a sorted, non-overlapping list

No sort needed, one pass, three phases: copy the intervals that end before the new one starts; absorb every interval that overlaps or touches the new one, widening it; copy the rest.

### Peak overlap: the sweep line

"How many rooms do I need?" is "what is the largest number of intervals active at the same instant?". Turn each interval into two **events**: `+1` at its start, `−1` at its end. Sort the events by time and walk through them with a running count; the answer is the largest value the count reaches.

At equal times the order matters. With half-open intervals, a meeting that ends at 3 has left the room before one that starts at 3. So ends are processed **before** starts at the same time. Sorting tuples `(time, delta)` does it for free, since `−1 < +1`:

```python
sorted([(3, +1), (3, -1), (1, +1)])        # [(1, 1), (3, -1), (3, 1)]
```

### A booking calendar

Accept a booking only if it overlaps none of the existing ones. Keep the bookings sorted by start. A new booking can only collide with its two neighbours in that order: the one just before and the one just after. **Binary search** finds its position in O(log n):

```python
import bisect
starts = [10, 20, 30]
bisect.bisect_left(starts, 25)      # 2: the new start would go at index 2, between 20 and 30
```

Check the neighbour at `i − 1` (does it end after the new start?) and the neighbour at `i` (does it start before the new end?).

### Traps of the day

- Sorting by end.
- Extending with the next end instead of the maximum of the two ends.
- `<` against `<=`: decide from the convention, then test with touching intervals.
- Starts processed before ends at the same time in the sweep.
- Checking only one neighbour in the calendar.

### Today's build

| Piece | Job | Lesson section |
|---|---|---|
| `merge` | merge overlapping or touching intervals | merge |
| `insert` | add one interval to a sorted list, O(n) | insert |
| `max_concurrent` | peak overlap | the sweep line |
| `Calendar.book` | accept or refuse, O(log n) search | a booking calendar |

Run: `uv run pytest weeks/w1-coding-base/d5-intervals -k "not review"`

---

## End of the week

- **AI-off gate (15 min):** one drill from `drills/w01`, timer on, AI fully off: `uv run pytest drills/w01 -k d<number>`. Protocol: `drills/README.md`.
- **Reading slot (20 min, read only):** this week's file is row 1 of `reading/README.md`.
- **Ship one public thing** and log it in `SHIPLOG.md`: one claim, one piece of evidence. A write-up of this week's hardest lab with its numbers counts.
- **Tick `PROGRESS.md`**, write the retro, and name the hardest lab: next Monday you rewrite its main function from a blank file.

You are done with week 1 when you can do these without notes:

- [ ] write push, pop and heapify, and explain why heapify is O(n)
- [ ] explain why top-k largest uses a min-heap
- [ ] explain tombstones with a three-key example, and when and how a table resizes
- [ ] draw the LRU structure and write `get` and `put` in O(1)
- [ ] explain why a path in a trie is not a word, and how delete prunes
- [ ] merge intervals, and compute a peak overlap with a sweep line, stating your convention
- [ ] narrate a solution in the five steps

## Optional depth (not needed for the labs)

- Python details that come up in interviews, with questions and short answers: `knowledge/01-python-for-interviews.md`
- Patterns behind the drills: `drills/PATTERNS.md`
- Next week: [`../w2-reliability/README.md`](../w2-reliability/README.md)
