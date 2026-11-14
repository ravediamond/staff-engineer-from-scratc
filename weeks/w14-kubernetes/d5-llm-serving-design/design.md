# Friday design #8: host and fine-tune LLMs on Kubernetes

**Timer: 45 minutes. Write in `my_design.md`. Use the 45-minute frame (`knowledge/05`).**

## Prompt

Your company (60,000 people, EU, regulated industrial data) wants an internal platform to **serve** and
**fine-tune** open-weight LLMs on Kubernetes. Year one: three served models (an 8B, a 32B and a 70B),
40 internal applications, about 300 requests per second at peak for the small model and 20 for the large
one, interactive SLO of 500 ms time-to-first-token at p95. Fifteen teams want to fine-tune (mostly LoRA)
on their own data; a few need full fine-tuning of the 8B. You have 64 H100-class GPUs reserved in one EU
region and may burst on spot capacity. Data must stay in the EU.

Design the platform.

## What the interviewer will push on

- Derive the GPU count per model. What caps concurrency?
- What do you autoscale on, and what happens during a 5× spike?
- How does a request find the right replica? Why not a plain Service?
- How are GPUs shared between serving and fifteen fine-tuning teams? Who gets preempted?
- A distributed fine-tuning job gets 3 of its 4 workers. Then what?
- How does a fine-tuned model reach production, and what stops a bad one?
- Cold start of the 70B. Scale to zero?
- A GPU throws Xid errors at 3 a.m. A region-wide spot reclaim hits your training pool.
- Cost per million tokens, and the first three things you would cut.
- What would you buy instead of build?

## Deliverable

Requirements and numbers → diagram (serving path, fine-tuning path, platform layer) → request path →
GPU scheduling and autoscaling → fine-tuning lifecycle → failure modes → cost → v1 scope and what you
would not build. Then grade yourself with `rubric.md`.
