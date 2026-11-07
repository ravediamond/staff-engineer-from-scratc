# 14. Reading maps (for the weekly reading slot)

Read the file first, write your 10-line note, **then** compare with the map below. Versions drift: if lines moved,
search for the named function or class.

| Week | File | What you should have found |
|---|---|---|
| 1 | CPython `Objects/dictobject.c` (comments at the top) | compact dict layout (indices + entries), open addressing with perturbation, resize policy, why iteration is insertion-ordered |
| 2 | `tenacity` (`tenacity/__init__.py`, `wait.py`) | retry policy objects composed (stop, wait, retry predicates), full jitter implementation, how `Retrying` handles exceptions vs results |
| 3 | etcd `raft/log.go` and `raft/raft.go` (`maybeCommit`, `handleAppendEntries`) | log matching, conflict truncation, commit only for the current term (`matchTerm` check), unstable vs stable entries |
| 4 | FAISS `IndexIVF.cpp` (`search_preassigned`) or Qdrant HNSW search | coarse quantizer assignment, nprobe loop, inverted list scanning, result heap |
| 5 | Kueue docs + `pkg/scheduler/scheduler.go` | admission by quota, cohorts and borrowing, preemption candidates, why gang admission is all-or-nothing |
| 6 | LlamaIndex or Haystack hybrid retriever + reciprocal rank fusion code | how ranks are fused, default k, where metadata filters are applied (pre or post) |
| 7 | `lm-evaluation-harness` `evaluator.py` | task loading, request batching, how metrics and stderr are computed (bootstrap for some metrics) |
| 8 | TRL `trl/trainer/reward_trainer.py` and `dpo_trainer.py` (loss) | pairwise loss with optional margin, `center_rewards`, DPO loss variants and where the reference log-probs come from |
| 9 | PyTorch `torch/nn/parallel/distributed.py` (Reducer usage) + torchtitan `parallelize` | bucketing, `no_sync`, gradient division by world size, how FSDP2/TP are composed |
| 10 | vLLM `core/scheduler.py` (or `v1/core/sched/scheduler.py`) and the KV block manager | continuous batching decisions each step, preemption (swap vs recompute), block allocation and prefix caching |
| 11 | pstack's skills and principles (its public repository) | how principles are phrased, how the router picks a playbook, what a verification skill checks, what you would adopt and what you would change |
| 12 | Your own agentic harness at work (or your best OSS project) | apply W10's checklist: validation, budgets, retries location, idempotency, tracing, sandbox, verification; list the three gaps |
