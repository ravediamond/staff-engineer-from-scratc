# Friday design #7: an event-driven order platform on Kafka

**Timer: 45 minutes. Write in `my_design.md`. Use the 45-minute frame (`knowledge/05`).**

## Prompt

A retailer's order service runs on Postgres. Today it calls inventory, notifications, fraud, search
indexing and the data warehouse synchronously, and every incident in one of them breaks checkout.
Peak: 20,000 order events per second, 1 KB each. Inventory must never apply an event twice or out of
order for the same order. Analytics wants per-minute revenue within 30 seconds. Six teams will consume
the events and deploy independently.

Design the event backbone. "Use Kafka" is the first sentence, not the answer.

## What the interviewer will push on

- How does an order change reach Kafka without loss or phantom events?
- Partition key, partition count, and what happens when you need more partitions.
- `replication.factor`, `min.insync.replicas`, `acks`: what failure does your choice survive?
- Delivery semantics per consumer. Where is "exactly-once" real and where is it idempotency?
- A handler bug poisons one message. A downstream system is down for 2 hours. What happens?
- A team wants to add a field; another wants to rename one.
- How do you know it is healthy? What do you page on?
- Would you still choose Kafka for 50 events per second?

## Deliverable

Requirements and numbers → diagram → the path of one event → failure handling → evolution and
operations → what you would not build in v1. Then grade yourself with `rubric.md`.
