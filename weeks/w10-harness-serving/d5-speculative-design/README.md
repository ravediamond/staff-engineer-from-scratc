# W10 D5: speculative decoding + Friday design + your own skill set

Primer: `knowledge/11-llm-serving.md` §4. Reference: Leviathan et al. (2023), Chen et al. (2023).

## The one idea

A small **draft** model proposes k tokens cheaply; the big **target** model verifies all k in one
forward pass. The acceptance rule makes the output distribution **exactly** the target's:

```
for each drafted token x (draft prob q(x), target prob p(x)):
    accept with probability min(1, p(x) / q(x))
    on rejection: sample from the residual  norm(max(0, p − q)), and stop
if all k accepted: sample one extra token from the target's next distribution (free)
```

With acceptance rate α per token, expected tokens per target pass = `(1 − α^(k+1)) / (1 − α)`.
Speedup ≈ that divided by `(1 + k·c)`, where c = draft cost / target cost.

## Today's build (`w10d5_speculative.py`)

`speculative_step(p_dists, q_dists, drafted, rng)` → emitted tokens, `expected_tokens(alpha, k)`, `speedup(alpha, k, c)`.
The test checks the **distribution** of the first emitted token matches p over 20,000 trials.

## Friday design (45 min)

`design.md`: an agentic coding assistant and its evaluation. Timer, `my_design.md`, `rubric.md`, model answer on `solutions`.

## Ship this week: your own skill set (pstack-style)

Lauren Tan's pstack is a set of agent skills encoding how she works: principles ("Prove It Works",
"Fix Root Causes"), playbooks (bug fix, feature, refactor, perf), verification skills. Build yours,
public, in a new repo (`ravediamond/rstack` or any name):

1. **Principles** (10–15): your rules, each one sentence + one example from your work. Start from what
   this repo drilled: invariants first, predict before running, paired comparisons, idempotent side
   effects, retries at one layer, eval before claims.
2. **Playbooks** (5): eval regression triage, RAG retrieval miss, flaky agent run, training loss spike,
   new tool integration. Each: trigger, steps, verification, done criteria.
3. **Verification skills** (2+): e.g. "prove this RAG change is better" (runs the W6/W7 tooling, outputs CIs),
   "check this distributed training change" (W9 equivalence tests).
4. A README that says what it is, how to install it in Claude Code, and one before/after example.

Add the link to `SHIPLOG.md`. This is the single most "Lauren-level" artifact in the 12 weeks.

## Staff angle

Speculative decoding is a pure systems win (identical outputs, lower latency), which makes it a good
interview topic: it tests whether you understand that the acceptance rule preserves the distribution.
The staff judgment is when it pays: high acceptance (predictable text, code, structured output), spare
compute (latency-bound low-batch serving), and a draft much cheaper than the target. At high batch sizes
the target is already efficient and the gain shrinks.
