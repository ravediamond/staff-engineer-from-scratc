# Questions

1. What is the dual-write problem? Why can a try/except with a retry not fix it?
2. Describe the outbox pattern with CDC end to end. What are the delivery semantics at each hop?
3. BACKWARD vs FORWARD compatibility: which side deploys first in each, and which changes are always safe?
4. "Exactly-once": what does Kafka guarantee with transactions, and what remains your job?
5. Kafka vs RabbitMQ/SQS vs Pub/Sub/Kinesis vs Postgres `SKIP LOCKED`: one sentence each on when to choose it.
6. A poison message makes a consumer crash in a loop. Design the retry and dead-letter path without blocking the partition forever and without losing per-key order where it matters.

