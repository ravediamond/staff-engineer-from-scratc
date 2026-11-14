# Hands-on Kafka (after W13 D3)

Not executed by the author of this repo (see `handson/README.md`). Docs: https://kafka.apache.org/documentation/

All commands run **inside** a broker container, so no host networking setup is needed:

```bash
cd handson/kafka
docker compose up -d
alias k1='docker compose exec kafka-1'
K=/opt/kafka/bin
B="--bootstrap-server kafka-1:9092,kafka-2:9092,kafka-3:9092"
```

## Session 1: the log, replication, acks (maps to W13 D1–D2)

1. Create and inspect. Predict the output of `--describe` first: how many leaders per broker?
   ```bash
   k1 $K/kafka-topics.sh $B --create --topic orders --partitions 3 --replication-factor 3 --config min.insync.replicas=2
   k1 $K/kafka-topics.sh $B --describe --topic orders        # Leader, Replicas, Isr per partition
   ```
2. Produce with keys, consume from the beginning, and look at which partition each key lands on.
   ```bash
   k1 $K/kafka-console-producer.sh $B --topic orders --property parse.key=true --property key.separator=:
   # type: o1:created  o2:created  o1:paid  o1:shipped   (Ctrl-D to end)
   k1 $K/kafka-console-consumer.sh $B --topic orders --from-beginning --property print.key=true --property print.partition=true --property print.offset=true
   ```
   Check: are o1's three events on one partition, in order?
3. **Kill a broker.** Predict the ISR and the leaders, then look.
   ```bash
   docker compose stop kafka-2
   k1 $K/kafka-topics.sh $B --describe --topic orders        # ISR shrinks, leaders move
   ```
   Produce with `--producer-property acks=all`: it works (ISR = 2 ≥ min ISR).
4. **Kill a second broker.** Predict: does an `acks=all` produce succeed? Does `acks=1`?
   ```bash
   docker compose stop kafka-3
   k1 $K/kafka-console-producer.sh --bootstrap-server kafka-1:9092 --topic orders --producer-property acks=all
   ```
   Expected: `NotEnoughReplicasException` after retries. Note also what happened to the KRaft controller
   quorum with 1 of 3 voters left (can you create a topic now?). Bring both back:
   `docker compose start kafka-2 kafka-3`, watch the ISR grow again.
5. Look at the files. Find the `.log`, `.index` and `.timeindex` of a partition and dump a segment:
   ```bash
   k1 sh -c 'ls /tmp/kraft-combined-logs/orders-0 2>/dev/null || find / -type d -name "orders-0" 2>/dev/null'
   k1 $K/kafka-dump-log.sh --print-data-log --files <path>/00000000000000000000.log
   ```
   Find: base offset, producer id and sequence numbers of each batch (the idempotent producer of D3).

Write down: the exact error text at step 4 and the ISR you saw at each step.

## Session 2: groups, lag, rebalances, compaction (maps to W13 D3, D1)

1. Start two consumers in the same group in two terminals; produce 20 keyed records; see the split.
   ```bash
   k1 $K/kafka-console-consumer.sh $B --topic orders --group inventory --property print.partition=true
   k1 $K/kafka-consumer-groups.sh $B --describe --group inventory     # CURRENT-OFFSET, LOG-END-OFFSET, LAG, owner
   ```
2. Stop one consumer. Predict what `--describe` shows 10 seconds later, then run it. Start a third and
   fourth consumer: with 3 partitions, what does the fourth do?
3. Lag: stop all consumers, produce 1,000 records
   (`k1 $K/kafka-producer-perf-test.sh --topic orders --num-records 1000 --record-size 200 --throughput -1 --producer-props bootstrap.servers=kafka-1:9092`),
   read the lag, restart a consumer, watch it fall.
4. Reset offsets (the replay button): `kafka-consumer-groups.sh ... --group inventory --topic orders --reset-offsets --to-earliest --execute` (group must be inactive).
5. Compaction: create `--config cleanup.policy=compact --config segment.ms=10000 --config min.cleanable.dirty.ratio=0.01`,
   write the same key 50 times then a tombstone for another key (`kcat` or a 5-line Python client makes
   null values easy), wait, consume from the beginning. How many records are left for the key? Which offsets?
6. Optional (Kafka 4.2+): share groups. `kafka-console-share-consumer.sh` with two consumers on a
   1-partition topic: both receive records. Compare with step 2.

## Session 3 (optional): outbox with Debezium

Add Postgres (with `wal_level=logical`) and a Kafka Connect container with the Debezium Postgres
connector; follow the Debezium tutorial and its outbox event router:
https://debezium.io/documentation/reference/stable/tutorial.html ·
https://debezium.io/documentation/reference/stable/transformations/outbox-event-router.html
Goal: insert an order + outbox row in one transaction, see the event on a topic; kill Connect between
two inserts and check that nothing is lost and what is duplicated.

Clean up: `docker compose down -v`.
