# Part 2 roadmap: closing every blind side

Part 1 (weeks 1–12) covers the coding base, reliability, distributed primitives and the five
specialities. A gap analysis against 2025–2026 staff loops (Google L6, Meta E6, Paris scale-ups) found
24 missing tracks. Part 2 adds them. No week limit: completeness wins.

Status: ✅ in the repo · ⏳ next · 📋 planned.

| # | Track | Where | Status |
|---|---|---|---|
| G1 | Kafka internals ("design Kafka") | `weeks/w13-streaming` d1–d3, `knowledge/16`, `handson/kafka` | ✅ |
| G2 | Stream processing, CDC/outbox, schemas | `weeks/w13-streaming` d4–d5 + design #7 | ✅ |
| G3 | Kubernetes core | `weeks/w14-kubernetes` d1–d3, `knowledge/17`, `handson/k8s` | ✅ |
| G4 | Kubernetes for ML: GPUs, quotas, gangs | `weeks/w14-kubernetes` d4, `knowledge/18` | ✅ |
| G5 | LLM serving on Kubernetes | `weeks/w14-kubernetes` d5 + design #8 | ✅ |
| G6 | Fine-tuning platform (LoRA, QLoRA, promotion gate) | week 16 | ⏳ |
| G7 | Databases: MVCC, isolation, B+tree, SQL, replication, ledger and holds | `weeks/w15-databases`, `knowledge/19` | ✅ |
| G9 | Recommenders, ranking, ML breadth (two-tower, logQ, IPS, calibration) | week 16 | ⏳ |
| G11 | Observability, SLOs, burn rates, incident response, DR | week 16 | ⏳ |
| G8 | Classic design breadth (booking, ledger, geo, CRDT, TSDB, object store, crawler, notifications, cache) | weeks 17–18 | 📋 |
| G10 | AI-assisted coding rounds (multi-file codebases, timed) | week 19 | 📋 |
| G12 | Networking and API layer (load balancing, SSE, OAuth2/JWT, gRPC) | week 19 | 📋 |
| G13 | Security, privacy, EU regulation (prompt injection, erasure, AI Act) | week 20 | 📋 |
| G14 | LLM gateway and LLMOps | week 20 | 📋 |
| G15 | Inference optimisation and GPU basics (roofline, quantisation, FlashAttention) | week 21 | 📋 |
| G16 | Agent infrastructure (durable execution, MCP) | week 21 | 📋 |
| G17 | Coding breadth (graphs, DP, binary search, concurrency, OO design): 40 drills | drills w13+ | 📋 |
| G18 | Containers, Linux, performance | week 22 | 📋 |
| G19 | Cloud, IaC, CI/CD, GitOps | week 22 | 📋 |
| G20 | MLOps breadth (point-in-time joins, drift, shadow/canary) | week 23 | 📋 |
| G21 | Data orchestration (DAGs, backfills, lakehouse) | week 23 | 📋 |
| G22 | Parallelism beyond DDP/ZeRO (TP, PP, layouts) | week 24 | 📋 |
| G23 | RL post-training (GRPO, verifiable rewards) | week 24 | 📋 |
| G24 | Staff behaviours II (strategy doc, TCO, past-project presentation) | week 25 | 📋 |

Order of work if an interview is close: G1–G5 and G7 (done) → G9 → G8 → G11 → G6 → the rest.
`SELF_AUDIT.md` is the checklist: every line you cannot answer out loud in two minutes is a blind side.
