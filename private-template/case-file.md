# Case file: <project name>

Fictional, fully worked example. Copy the structure, write your own.

## One-line summary
Retrieval-augmented assistant for maintenance procedures; moved answer accuracy from 61% to 84% on a
held-out set and cut median latency from 4.1 s to 1.6 s.

## Context (2 min version)
- Users: 1,200 field technicians, 9 countries, 4 languages.
- Before: keyword search over 40k PDFs; technicians called experts for 30% of interventions.
- Constraint: documents have per-site access control; answers must cite the procedure page.

## My role
Tech lead, 4 engineers, no product manager for the first 3 months. I wrote the design, owned eval.

## Decisions (each: options, choice, why, what it cost)
1. **Chunking by section headings instead of fixed tokens.** Options: 512-token fixed, recursive,
   heading-aware. Chose heading-aware: +7 points recall@10 on our set (CI 4–10). Cost: a parser per
   document family (3 weeks).
2. **ACL filtering inside the vector search, not after.** Post-filtering returned 2.3 results on
   average instead of 10 for restricted users. Cost: index rebuild, metadata on every vector.
3. **Abstain when no chunk passes a support threshold.** Cut wrong-but-confident answers from 9% to
   3% at the price of 11% abstentions. Product agreed after seeing 20 examples side by side.

## Numbers I will say (and how to re-derive them)
| Number | Source | Re-derive |
|---|---|---|
| 61% → 84% accuracy | eval run 2025-03-02 vs 2025-06-14, 412 questions | `eval/report.py --runs a b` |
| 4.1 s → 1.6 s p50 | Grafana dashboard export | latency CSV in `data/` |

## What went wrong
The first eval set was written by the team, not by technicians: it overestimated accuracy by 12
points. Fixed by sampling real questions from call logs.

## What I would do differently
Put the eval set in front of users in week 1, not week 8.

## Deep-dive questions I expect (and my 60-second answers)
- "Why not fine-tune instead of RAG?" → documents change weekly, ACL per site, citations required.
- "How did you know 84% was real?" → held-out set from call logs, 2 annotators, kappa 0.78, bootstrap CI 80–87.
