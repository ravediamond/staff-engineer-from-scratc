# Friday design #3: evaluation infrastructure for an AI product

**Timer: 45 minutes. Write in `my_design.md`.**

## Prompt

A consumer AI assistant has 1M weekly users. Thirty teams change prompts, tools, retrieval and
models, collectively ~40 changes per week. Today each team has its own notebook evals; two
regressions reached users last month (one in a non-English market, one a latency blow-up from a
tool loop). Leadership asks you to design the evaluation platform and process, offline and online.

## What the interviewer will push on

- What is a "test case" and who owns the datasets? How do they stay representative?
- How do you gate 40 changes a week without becoming the bottleneck?
- LLM judges: how do you trust them?
- How does offline connect to online? How would you know your offline eval is any good?
- Cost: running evals is not free. Budget?
- What happens when a team disagrees with the gate?

## Deliverable

Requirements and non-goals · estimation (eval runs/week, cost) · data model (case, dataset version,
run, result) · architecture · two deep dives · metrics and process (governance), scope.
