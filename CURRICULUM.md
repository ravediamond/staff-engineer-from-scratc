# Curriculum: 12 weeks, 60 sessions

Each lab: README (concept + staff angle) → predict.md / predict_run.py → build with tests → review (planted bug) →
questions.md (out loud). Fridays of weeks 5–10 add a 45-minute written design graded with a rubric. Model answers
and solutions: `solutions` branch. Weekly: 4 drills, 1 reading slot, 1 public ship. K = knowledge primer of the week.

## Week 1: coding base and communication · K: `01`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 heap | MinHeap, O(n) heapify, heap sort, top-k | sift-down always takes the left child |
| Tue | d2 hash map | open addressing, tombstones, resize | delete empties the slot |
| Wed | d3 LRU & TTL | O(1) LRU with sentinels, lazy-expiry TTL cache | get does not refresh recency |
| Thu | d4 trie | counts, pruning delete, top-k autocomplete | prefix word inserted later never marked |
| Fri | d5 intervals | merge, insert, sweep-line peak, calendar | merge sorted by end |

## Week 2: reliability primitives · K: `02`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 retries | full jitter, deadlines, retry budget | retries 4xx |
| Tue | d2 circuit breaker | closed/open/half-open with trial limit | unlimited half-open trials |
| Wed | d3 idempotency | key + fingerprint store, exactly-once ledger | no fingerprint check |
| Thu | d4 rate limiting | token bucket, sliding log, sliding counter | refill not capped |
| Fri | d5 asyncio | bounded map, multi-stage pipeline, settled gather | unbounded queue |

## Week 3: distributed primitives · K: `03`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 consistent hashing | ring + vnodes, rendezvous, movement, balance | no wrap-around |
| Tue | d2 quorums | N/R/W cluster, read repair | first response wins |
| Wed | d3 clocks | Lamport, vector clocks, siblings | merge keeps the "bigger" clock |
| Thu | d4 Raft log | AppendEntries, leader backoff, commit rule | Figure 8 |
| Fri | d5 leases | lock service with fencing tokens, fenced storage | highest token not remembered |

## Week 4: storage and retrieval · K: `04`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 WAL & LSM | torn-tail replay, memtable, SSTables, recovery | oldest SSTable first |
| Tue | d2 Bloom & compaction | optimal params, double hashing, k-way merge | oldest version kept |
| Wed | d3 BM25 | inverted index, BM25, boolean AND | length normalisation inverted |
| Thu | d4 vector search | exact, k-means, IVF, NSW graph, recall@k | dot product as cosine |
| Fri | d5 caches & consumers | single-flight cache, exactly-once consumer | commit before process |

## Week 5: system design method · K: `05`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 estimation | QPS, storage, bandwidth, LLM GPUs, cost | bytes reported as bits |
| Tue | d2 IDs & pagination | base62, Snowflake, opaque keyset cursors | overlapping Snowflake fields |
| Wed | d3 news feed | hybrid fan-out, capped inboxes, k-way merge | oldest first |
| Thu | d4 chat | per-conversation seq, idempotent sends, receipts, presence | read pointer moves back |
| Fri | d5 job scheduler + **design #1** | leases + tokens, retries, DLQ, delayed jobs; ML job scheduler design | stale lease completes |

## Week 6: RAG · K: `06`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 chunking | fixed, recursive, heading-aware, offsets | stride = size + overlap |
| Tue | d2 hybrid | hashed embeddings, RRF, min-max fusion | scores instead of ranks |
| Wed | d3 metrics | recall, MRR, nDCG, rerank, bootstrap CI | IDCG from retrieved list |
| Thu | d4 freshness | versioned index, tombstones, staleness | older update overwrites |
| Fri | d5 ACL & citations + **design #2** | ACL pre-filter, citation support, abstention, cost; enterprise RAG design | post-filter after top-k |

## Week 7: evaluation and experimentation · K: `07`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 harness | repeats, flaky cases, slices, paired bootstrap, gate | unpaired bootstrap |
| Tue | d2 judges | confusion, κ, weighted κ, position bias | chance agreement from one rater |
| Wed | d3 statistics | Wilson, McNemar, Holm, sample size, MDE | McNemar over all pairs |
| Thu | d4 online A/B | SRM, z-test, CUPED, peeking simulation | θ uses var(y) |
| Fri | d5 offline↔online + **design #3** | Kendall, Spearman, sign agreement, launch rule; eval platform design | τ denominator |

## Week 8: reward models · K: `08`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 Bradley–Terry | BT fit in PyTorch, Elo | sign flipped |
| Tue | d2 pairwise RM | MLP RM, pairwise loss, prompt split, accuracy | split by pair |
| Wed | d3 calibration | ECE, temperature scaling, length bias | unweighted ECE |
| Thu | d4 best-of-N | BoN KL, over-optimisation curve | evaluate with the selector |
| Fri | d5 DPO & PRMs + **design #4** | DPO on a tabular policy, PRM aggregation; RM pipeline design | no reference model |

## Week 9: distributed training · K: `09`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 collectives | ring reduce-scatter + all-gather, byte counts | chunk index off by one |
| Tue | d2 DDP | 2-process gloo == single process | sum not mean |
| Wed | d3 resume | full-state atomic checkpoint, bit-exact resume | optimizer not saved |
| Thu | d4 ZeRO | memory table, ZeRO-1 step == Adam | Adam counted once |
| Fri | d5 checkpoints + **design #5** | sharded save, manifest, reshard, MFU; training platform design | manifest trusted blindly |

## Week 10: harness engineering and serving · K: `10`, `11`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 agent loop | schema validation, errors as observations, budgets | extra step |
| Tue | d2 sandbox | containment, command policy, bounded execution | startswith check |
| Wed | d3 tracing & replay | spans, recorder, hermetic replayer, trace diff, cost | replay by name only |
| Thu | d4 serving math | KV sizing, static vs continuous batching, paging | K and V counted once |
| Fri | d5 speculative + **design #6** + **your skill set** | exact acceptance rule, speedup; coding-agent design; ship your pstack-style skills | ratio inverted |

## Week 11: staff judgment and behavioral · K: `12`, `principal/`
| Day | Lab | Build | Review bug |
|---|---|---|---|
| Mon | d1 root cause | flaky-aware bisect, change point, event correlation | returns lo |
| Tue | d2 prove it works | property-based testing with shrinking | shrinker never moves |
| Wed | d3 design docs | RFC linter; write your RFC | headings in code blocks |
| Thu | d4 migrations | versioned backfill, verify, gated state machine | ungated cutover |
| Fri | d5 STAR bank | validation, coverage vs rubrics, story picker | stories without results counted |

## Week 12: mocks · K: `13`
| Day | Round |
|---|---|
| Mon | coding A: time-versioned KV + task scheduler, 35 min |
| Tue | coding B: Misra–Gries + word ladder, 35 min; review a candidate |
| Wed | system design (feature store) + ML design (ticket triage), 2 × 45 min |
| Thu | behavioral + project deep dive, scored with the calibrated scorer |
| Fri | take-home (4 h) + pair programming on an existing codebase + final retro |

## Drills (4 per week): `drills/w01` … `drills/w12` · Reading slot: `reading/` · Ship log: `SHIPLOG.md`

## After week 12
Repeat the weakest round weekly, keep shipping weekly, apply to three companies, and start `principal/05-exercises.md`.
