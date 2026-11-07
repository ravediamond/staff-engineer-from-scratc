# Model answer: feature store (staff level)

**Requirements.** Feature definitions as code (owned, versioned, reviewed); batch + streaming
computation; online serving p99 < 10 ms at 20k predictions/s (batched lookups); offline point-in-time
joins; reuse via a registry. Non-goals: model serving, feature discovery UI beyond a registry v1.

**Estimation.** Online: 200M entities × 300 features × 8 B ≈ 480 GB per replica, ~1.4 TB with 3
replicas: a sharded KV store (Redis cluster on RAM is expensive at this size; DynamoDB/Bigtable/ScyllaDB
or Redis on flash). 20k predictions/s with one batched multi-get per entity per model ≈ 20–60k reads/s:
easy if batched, 6M reads/s if not. Offline: daily snapshots in Parquet partitioned by date + event logs.

**Design.** Feature definitions (SQL/Python transforms with entity, timestamp, TTL) in a registry →
batch engine (Spark/warehouse) writes to the offline store and materializes the latest values to the
online store; streaming engine (Flink) updates online values and appends to the offline log. Serving SDK
does one multi-get per entity. Training: point-in-time join of labels (entity, event_ts) against feature
history with `feature_ts <= event_ts` (as-of join), never using later values.

**Deep dive: training/serving skew.** One definition compiles to both batch and streaming paths (or
streaming-only with backfill from logs); log the features actually served at prediction time and train on
those logged values when possible ("log and wait"); monitor online vs offline value distributions per
feature (PSI) and alert on skew.

**Deep dive: backfills and definition changes.** Definitions are immutable and versioned
(`user_txn_7d:v2`); a new version is backfilled offline from raw events, validated (distribution vs v1,
model offline eval), materialized online, then consumers migrate; v1 is deprecated with usage tracking
(W11 D4 pattern).

**Operations.** Freshness SLOs per feature, ownership per feature group, cost per feature (unused
features get deprecated), access control on sensitive features. Build vs buy: Feast/Tecton/Databricks
feature store vs internal; buy the online/offline plumbing, own definitions and governance.
