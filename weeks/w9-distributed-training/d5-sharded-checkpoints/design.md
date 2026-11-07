# Friday design #5: multi-node training platform

**Timer: 45 minutes. Write in `my_design.md`.**

## Prompt

Your company is buying 512 H100s (64 nodes × 8, InfiniBand) to train and fine-tune models from 1B
to 70B parameters. Today researchers run ad-hoc scripts on single nodes. Design the training
platform: job submission to multi-node execution, data loading, checkpointing, failure recovery,
experiment tracking, and how you will know the cluster is used well.

## What the interviewer will push on

- Hardware fails. How often at this scale, and what happens to a 3-week run?
- What parallelism strategy for 7B vs 70B, and who decides?
- Checkpointing: where, how often, how fast, and how do you know a checkpoint is good?
- Data pipeline: how do you keep 512 GPUs fed, and make data order reproducible?
- What metrics prove the platform is good (and the $15M is not wasted)?

## Deliverable

Requirements and non-goals · estimation (failure rate, checkpoint size and time, data throughput) ·
architecture · two deep dives · metrics, risks, scope.
