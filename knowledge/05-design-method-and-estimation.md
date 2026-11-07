# 05. Design method and estimation

## §1 The 45-minute frame

Requirements (functional, non-functional with numbers, non-goals) → estimation → API and data model →
high-level design with one request walked end to end → two deep dives you choose by risk → wrap-up
(bottlenecks, monitoring, what you would not build). Drive it; check in with the interviewer at each transition.

## §2 Numbers to know

- 1 day ≈ 10⁵ s (86,400). 1 month ≈ 2.6 × 10⁶ s. 1M requests/day ≈ 12 QPS.
- Peak ≈ 2–10× average; say your factor.
- 1 char ≈ 1 byte (ASCII), 1 token ≈ 4 English chars ≈ 0.75 words; French and code use more tokens per word.
- A modern server: 32–128 cores, 256 GB–2 TB RAM, 10–100 Gb/s network.
- One H100: ~990 TFLOP/s dense bf16, 80 GB HBM at ~3.35 TB/s.
- Object storage ≈ $20/TB-month; a GPU hour ≈ $2–4 (cloud, on-demand varies a lot).

## §3 IDs, APIs, pagination

Snowflake/UUIDv7 for distributed, time-ordered IDs; base62 short codes; opaque keyset cursors; idempotency
keys on POST; versioned APIs; request ids in every response.

## §4 Feeds

Push (fan-out on write) vs pull (on read) vs hybrid with a celebrity threshold; capped inboxes; k-way merge;
ranking pipeline on top (candidate generation → ranking → filtering).

## §5 Chat and presence

Per-conversation sequence numbers from a single writer, idempotent sends with client ids, monotonic read
pointers, stateless gateways with resync by last seq, presence by heartbeats with TTL.

## §6 Schedulers

Leases with tokens, retries with DLQ, priorities, delayed jobs; at the platform level: quotas, fair share,
gang scheduling, preemption contracts.

## What interviewers write down (and you should do on purpose)

| Signal | Shows as |
|---|---|
| Drives the conversation | proposes the agenda, moves on without being pushed |
| Quantifies | numbers before boxes, uses them to choose |
| Trade-offs | "X because Y; it costs Z; I'd revisit if W" |
| Depth on demand | can go two levels down on any box |
| Pragmatism | buys or reuses the boring parts, builds the differentiating part |
| Operability | monitoring, rollout, failure modes without being asked |

## Questions

1. The interviewer says "design YouTube". What are your first three sentences?
<details><summary>Answer</summary>"That's broad, so let me scope it: upload, transcode, and watch with recommendations out of scope unless you want them. Are we optimizing for global playback latency or upload pipeline throughput? Here are the numbers I'll assume: 500M daily viewers, 500 hours of video uploaded per minute; I'll check those with you."</details>

2. How do you pick deep dives?
<details><summary>Answer</summary>By risk to the requirements: the component most likely to break the SLO, the cost driver, or the correctness-critical piece (consistency, permissions). Say it out loud: "The two risky parts are X and Y; I'll go deep on those unless you prefer something else."</details>

3. You realise at minute 30 that your design has a flaw. What do you do?
<details><summary>Answer</summary>Say it immediately, explain the flaw and its impact, propose the fix and what changes. Interviewers value self-correction; hiding it is worse than the flaw.</details>
