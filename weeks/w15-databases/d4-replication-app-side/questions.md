# Questions

1. Synchronous vs asynchronous replication: what does each guarantee at failover, and what does each cost?
2. Define read-your-writes and monotonic reads, with an implementation of each.
3. Walk through a failover. Where can data be lost, and what is split brain?
4. Sharding: range vs hash, how to pick a shard key, and what resharding costs.
5. PACELC: classify Postgres with async replicas, DynamoDB, Spanner, Cassandra.
6. You must run Postgres for a service with RPO = 0 and RTO < 60 s in one region. Describe the setup.

