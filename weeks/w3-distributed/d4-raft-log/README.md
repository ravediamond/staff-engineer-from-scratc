# W3 D4: Raft log replication and the commit rule

Primer: `knowledge/03-distributed-systems.md` §4. Reading slot week 9: etcd's `raft/log.go`.

## The one idea

Raft gives a cluster a single replicated log. A leader appends client commands, replicates them
with `AppendEntries`, and an entry is **committed** once it is stored on a majority. Two rules do
most of the work:

**1. Log matching (follower side).** `AppendEntries(term, prev_index, prev_term, entries, leader_commit)`:
- reject if `term < current_term` (stale leader);
- reject if the follower has no entry at `prev_index` with term `prev_term` (logs diverge before this point);
- otherwise, for each new entry: if an existing entry at that index has a **different term**, delete it
  **and everything after it**, then append; entries already present with the same term are kept
  (requests can arrive duplicated or reordered);
- `commit_index = min(leader_commit, index of last new entry)`.

**2. Commit only current-term entries by counting (leader side).** The leader advances
`commit_index` to the highest N such that a majority has `match_index >= N` **and
`log[N].term == current_term`**. Entries from older terms become committed indirectly, when a
current-term entry after them commits. Skipping the term check allows an entry stored on a
majority to be overwritten later (Raft paper, Figure 8).

Logs here are 1-indexed lists of `(term, command)`; index 0 is an implicit sentinel with term 0.

## Today's build (`w3d4_raft.py`)

- `Follower.append_entries(...) -> (success, match_index)`.
- `Leader`: `next_index`, `match_index` per follower; `request_for(f)` builds the AppendEntries args;
  `on_response(f, success, match_index)` updates or backs off `next_index`; `advance_commit()` with the term rule.
- `replicate_until_stable(leader, followers)` helper loop.

## Staff angle

You will not implement Raft at work. You will choose systems built on it (etcd, Consul,
CockroachDB, TiKV, Kafka KRaft) and debug them. Interviewers check that you know what consensus
costs: a majority round-trip per write (cross-region: ~100 ms), leader as bottleneck, and that 5
nodes tolerate 2 failures, not 4. In ML infra, the metadata store for your training cluster or
feature registry is Raft-backed. Put training *data* through it and you have built a bottleneck.
