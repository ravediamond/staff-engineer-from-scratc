# W5 D5: job scheduler (leases, retries, DLQ) + Friday design

Primer: `knowledge/05-design-method-and-estimation.md` §6.

## The one idea

Every ML platform has a job queue: eval runs, batch inference, embedding backfills,
fine-tuning jobs. The core is the same as SQS or Celery:

- **Lease (visibility timeout):** a worker takes a job for `lease_seconds`; if it does not complete
  in time, the job becomes available again (the worker probably died).
- **Lease token:** each lease gets a fresh token. `complete(job, token)` is rejected if the token is
  not the **current** lease, or a slow worker whose lease expired could complete a job that another
  worker is now running (W3 D5's fencing idea again).
- **Retries + dead-letter queue:** a job that fails or expires `max_attempts` times goes to the DLQ for
  a human, instead of poisoning the queue forever.
- **Priorities + FIFO within priority + delayed jobs** (`run_at`).

## Today's build (`w5d5_jobs.py`)

`JobQueue(lease_seconds, max_attempts, clock)`: `submit(job_id, priority, run_at=0)`, `lease(worker) -> (job_id, token) | None`,
`complete(job_id, token) -> bool`, `fail(job_id, token)`, `reap()` (expire leases), `dlq`, `state(job_id)`.

## Friday design (45 min, timed)

After the lab: open `design.md`, set a 45-minute timer, write your design in `my_design.md`, then
grade yourself with `rubric.md`. The model answer is on the `solutions` branch (`model_answer.md`):
read it only after grading.

## Staff angle

The scheduler is easy; the **policy** is the staff part: GPU quota per team, preemption of low
priority jobs, fairness (dominant resource fairness), gang scheduling for multi-node training
(all 64 GPUs or none), and what happens to a job's partial work when it is preempted
(checkpointing contract, W9 D5). Name the policy, the metric that shows it is fair, and the
escalation path when two teams both claim priority.
