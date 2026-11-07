# Take-home (4 hours): an eval CLI for a RAG endpoint

## Context
A team runs a RAG question-answering service behind `POST /ask {question} → {answer, citations[]}`.
They want a CLI to evaluate it before each deploy.

## Requirements
1. `evalrag run --dataset data.jsonl --endpoint URL --out results.jsonl`: calls the endpoint for each case
   with bounded concurrency (configurable), retries transient errors with backoff, and records latency.
2. Metrics per case: exact-match or contains-match against reference answers, citation validity (cited ids
   exist in the case's allowed documents), latency. Aggregate with bootstrap CIs; per-slice breakdown
   (`slice` field).
3. `evalrag compare a.jsonl b.jsonl`: paired comparison with a CI and a pass/fail gate (configurable tolerance).
4. Tests with a fake endpoint (no network in tests).
5. A README: how to run, design decisions, what you would do with more time.

## What reviewers look for
Correctness of the statistics (paired, not unpaired), robustness (timeouts, retries only on transient
errors, partial failure handling), code clarity, tests that would catch real bugs, and judgment in the
README about what was left out. Reuse what you built in W2, W6 and W7: that is the point.

## Timebox
4 hours. Write down what you skipped. Shipping a smaller, correct, tested tool beats a large, untested one.
