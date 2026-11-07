# Weekly reading slot (20 min, once a week, read only)

The labs train small, clean exercises. Real systems are thousands of lines you did not write. Reading them fast
and correctly is its own skill: it is how you review generated code, evaluate open-source dependencies, and show
depth in a deep-dive round. One real file per week.

## Protocol
1. Timer: 20 minutes. Read only. No running, no editing, no AI summary.
2. Fill `TEMPLATE.md` into `notes/wNN.md` (10 lines max).
3. Then (not before) compare with `knowledge/14-reading-maps.md`. Mark what you missed.
4. Log the time and misses in `PROGRESS.md`.

## Targets
| Week | Repository | File (search by name if lines moved) | Read for |
|---|---|---|---|
| 1 | python/cpython | `Objects/dictobject.c` (header comments) | how a production hash map is laid out |
| 2 | jd/tenacity | `tenacity/__init__.py`, `tenacity/wait.py` | composable retry policies, jitter |
| 3 | etcd-io/raft | `log.go`, `raft.go` (`maybeCommit`) | the commit rule you built in W3 D4 |
| 4 | facebookresearch/faiss | `faiss/IndexIVF.cpp` (`search_preassigned`) | IVF search at production quality |
| 5 | kubernetes-sigs/kueue | `pkg/scheduler/scheduler.go` | quota admission, borrowing, preemption |
| 6 | run-llama/llama_index or deepset-ai/haystack | hybrid retriever / RRF fusion | fusion defaults, filter placement |
| 7 | EleutherAI/lm-evaluation-harness | `lm_eval/evaluator.py` | how a widely used harness computes metrics and errors |
| 8 | huggingface/trl | `trl/trainer/reward_trainer.py`, DPO loss | real RM and DPO losses |
| 9 | pytorch/pytorch + pytorch/torchtitan | `torch/nn/parallel/distributed.py`; torchtitan `parallelize` | DDP reducer usage; composing FSDP2 + TP |
| 10 | vllm-project/vllm | scheduler + KV block manager | continuous batching and paging in production |
| 11 | pstack (Lauren Tan's skills, public repository) | the router skill, principles, one verification skill | how a top engineer encodes their workflow |
| 12 | your own harness or OSS project | the main loop | audit it with the W10 checklist |
