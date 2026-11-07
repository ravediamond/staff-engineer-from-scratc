# W1 D2: open-addressing hash map

Primer: `knowledge/01-python-for-interviews.md` §3.

## The one idea

A hash map is an array of slots plus a function `hash(key) % capacity` that says where to start
looking. Two families:

| | Separate chaining | Open addressing (today) |
|---|---|---|
| Collision | append to a list in the slot | probe the next slot (`i+1`, `i+2`… linear probing) |
| Memory | pointers, scattered | one flat array, cache-friendly |
| Delete | remove from list | **cannot just empty the slot**: put a **tombstone** |
| Used by | Java `HashMap` | CPython `dict`, Rust `HashMap` (SwissTable), Go maps since 1.24 |

**Invariant (linear probing):** if key `k` is stored at slot `j`, every slot from `hash(k) % cap` up to
`j` (wrapping) is occupied **or a tombstone**. That is why delete needs a tombstone: an empty slot in
the middle would make `get` stop early and miss keys stored after it.

**Load factor** `α = (live + tombstones) / capacity`. Expected probes for a miss with linear probing
≈ `1/2 · (1 + 1/(1-α)²)`. At α = 0.5 that is 2.5; at α = 0.9 it is 50.5. So: resize (double) when
α passes ~2/3, and rebuild without tombstones when you resize.

## Today's build (`w1d2_hashmap.py`)

`OpenAddressingMap` with `put`, `get` (KeyError if missing), `delete` (KeyError if missing),
`__len__`, `__contains__`, `keys()`. Linear probing, tombstones, resize ×2 when
`(live + tombstones) / capacity > 2/3`. A `probes` counter lets the tests check you do not scan
the whole table.

## Staff angle

The interview question behind the question is usually "what happens under adversarial keys?"
If an attacker controls keys and your hash is predictable, every key lands in the same slot and
every request is O(n): a hash-flooding DoS (it hit PHP, Java, Python, Ruby web servers in 2011).
Fix: seeded hashes (SipHash, Python's `PYTHONHASHSEED`). In distributed systems, the same idea
returns as "hot keys": one shard gets all the traffic. You will meet it again in W3 D1.
