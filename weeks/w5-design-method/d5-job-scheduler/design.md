# Friday design #1: a job scheduler for ML workloads

**Timer: 45 minutes. Write in `my_design.md`. Follow the 45-minute frame (week README).**

## Prompt

Your company runs ~50,000 ML jobs per day on a shared pool of 2,000 GPUs: evaluation runs
(minutes, 1 GPU), batch inference (hours, 1–8 GPUs), fine-tuning (hours to days, 8–64 GPUs,
multi-node). Twelve teams share the pool. Today it is a cron job plus a spreadsheet of who
gets which machines, and teams hoard GPUs "just in case".

Design the scheduler and the platform around it.

## What the interviewer will push on

- How do you stop one team from starving the others, and prove it is fair?
- A 64-GPU training job needs all 64 at once. How do you avoid it waiting forever behind small jobs?
- A node dies mid-training. What happens to the job?
- How do you preempt, and what contract does a preemptible job need to honour?
- What do you measure to know the platform is working (and the GPU spend is justified)?

## Deliverable

1. Requirements and non-goals (with numbers). 2. Estimation. 3. API and data model.
4. Architecture and one request end to end. 5. Two deep dives. 6. Metrics, risks, what you would not build.
