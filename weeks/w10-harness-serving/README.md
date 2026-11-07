# Week 10: harness engineering and serving

The harness is everything around the model that makes it a product: the loop, the tools, the
sandbox, the budget, the trace, the replay, the serving stack underneath. This is where staff
engineers in AI products spend their time, and where Lauren Tan's work (pstack, verification
loops, "loops you can trust") lives. This week builds each piece small enough to own completely,
then the serving math that decides what all of it costs.

Primer: `knowledge/10-harness-engineering.md` and `knowledge/11-llm-serving.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | agent loop: tool schemas, validation, errors as observations, step and token budgets | one extra tool call past max_steps |
| d2 | sandbox: path containment, command policy, timeouts, output caps | `startswith` path check is bypassable |
| d3 | tracing, recording and deterministic replay, trace diff, cost | replay matches by tool name only |
| d4 | serving math: KV cache, static vs continuous batching, paged blocks | KV cache forgets K *and* V |
| d5 | speculative decoding (exact) + **Friday design** + **your own skill set** | acceptance ratio inverted |
