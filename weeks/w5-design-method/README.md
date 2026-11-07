# Week 5: the system design method

Staff system design rounds are not about knowing more boxes. They are about running 45 minutes
like you would run a real design review: clarify what matters, put numbers on it, choose a
simple design, then go deep where the risk is, and say what you would not build. This week
installs the method and the estimation reflex, on four classic problems, each with a small
runnable core you can defend line by line. Friday is the first timed written design.

Primer: `knowledge/05-design-method-and-estimation.md` (read it on Monday's 2h day if you can:
it contains the 45-minute frame used by every Friday design from now on).

| Day | Lab | Review bug |
|---|---|---|
| d1 | back-of-the-envelope estimation, including LLM serving | bandwidth in bytes reported as bits |
| d2 | IDs (base62, Snowflake), cursor pagination | Snowflake fields overlap |
| d3 | news feed: fan-out on write vs read, hybrid | merged feed sorted oldest first |
| d4 | chat: per-conversation ordering, receipts, presence | read pointer can move backwards |
| d5 | job scheduler with leases, retries, DLQ + **Friday design** | stale lease can complete a job |

## The 45-minute frame (memorise it)

| Min | Phase | What a staff candidate does |
|---|---|---|
| 0–5 | Requirements | functional (3–5 bullets), non-functional with numbers (QPS, p99, durability, consistency), **explicit non-goals** |
| 5–10 | Estimation | users → QPS (avg, peak) → storage/yr → bandwidth → $ or GPUs. One line each, rounded. |
| 10–15 | API + data model | the 3–5 calls, the 2–4 tables or records, the access patterns |
| 15–25 | High-level design | simplest design that meets the numbers; walk one request end to end |
| 25–40 | Deep dives (2) | pick the two riskiest parts yourself (hot keys, consistency, failure, cost); trade-offs with numbers |
| 40–45 | Wrap-up | bottlenecks, what you would monitor, what you would build next, what you chose not to build |
