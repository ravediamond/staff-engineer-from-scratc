# Knowledge primers: the discussion rounds

The labs train your hands. The primers train what you must be able to **say**: mechanisms, the numbers
that matter, the trade-offs, and the follow-up questions interviewers use to find your edge. Each primer
ends with questions; answers are in collapsed `<details>` blocks.

| Primer | Week | What it covers |
|---|---|---|
| `01-python-for-interviews.md` | 1 | complexity cheat sheet, heaps, hash maps, LRU, tries, intervals, Python gotchas |
| `02-concurrency-and-reliability.md` | 2 | retries, deadlines, breakers, idempotency, rate limits, asyncio, backpressure |
| `03-distributed-systems.md` | 3 | partitioning, replication, clocks, consensus, leases, CAP/PACELC |
| `04-storage-and-retrieval.md` | 4 | WAL, LSM vs B-tree, Bloom filters, inverted indexes, ANN, caches, consumers |
| `05-design-method-and-estimation.md` | 5 | the 45-minute frame, numbers to know, classic designs |
| `06-rag.md` | 6 | chunking, hybrid retrieval, reranking, metrics, freshness, ACL, citations |
| `07-evaluation-and-experimentation.md` | 7 | eval harnesses, statistics, LLM judges, online experiments |
| `08-reward-models-and-preference-learning.md` | 8 | Bradley–Terry, RMs, calibration, over-optimisation, DPO, PRMs, verifiable rewards |
| `09-distributed-training.md` | 9 | collectives, DDP, resume, ZeRO/FSDP, TP/PP, checkpoints, MFU, goodput |
| `10-harness-engineering.md` | 10 | agent loops, tools, sandboxing, tracing and replay, verification |
| `11-llm-serving.md` | 10 | prefill/decode, KV cache, batching, paging, speculative decoding, routing |
| `12-staff-rubrics.md` | 11 | what Google, Meta and Paris unicorns assess at staff level; judgment habits |
| `13-question-bank.md` | 12 | mixed questions for mock warm-ups |
| `14-reading-maps.md` | any | what to look for in each reading-slot file |
| `15-staff-to-principal.md` | after 12 | what changes at principal, and how to get there |
| `16-streaming-and-messaging.md` | 13 | the log, ISR/HW/acks, producers and groups, stream processing, outbox/CDC, schemas, choosing a broker |
| `17-kubernetes.md` | 14 | control plane, control loops, workloads, scheduling, networking, rollouts, autoscaling, debugging |
| `18-ml-platform-on-kubernetes.md` | 14 | GPUs (device plugin, DRA, MIG), Kueue and gangs, training jobs, LLM serving, fine-tuning as a product |

## How to study a primer (30–45 min, on 2h days or weekends)

1. Read the mechanism sections once. Draw the diagrams yourself.
2. Close the file. Write the key equations and numbers from memory.
3. Answer the questions **out loud** before opening each answer. Mark: ✅ clean · 🟡 slow · ❌ did not know.
4. Re-ask only 🟡 and ❌ three days later, then a week later (spacing beats re-reading).

A precise 60-second answer followed by "I can go deeper on X" beats a five-minute tour.
