# Self-audit: no blind side

Answer each line **out loud in two minutes or less**, AI off. Mark ✅ clean · 🟡 slow or vague · ❌ could not.
Redo 🟡/❌ after 3 days, then after a week. "Where" points to the lab or primer; "roadmap" means the
material is not in the repo yet (`ROADMAP.md`): use the references in the primers meanwhile.

## Kubernetes core (W14 d1–d3, `knowledge/17`, `handson/k8s`)
- [ ] Trace `kubectl apply` to a running container, naming each component.
- [ ] Level- vs edge-triggered reconcile, with a failure of the second.
- [ ] Scheduler: filter vs score; three plugins of each.
- [ ] Requests vs limits; QoS classes; eviction order; throttling vs OOMKill.
- [ ] Liveness / readiness / startup probes and one misconfiguration of each.
- [ ] maxSurge / maxUnavailable for a 10-replica GPU service with no spare GPUs.
- [ ] HPA formula, tolerance, stabilization. KEDA and VPA in one sentence each.
- [ ] Cluster Autoscaler vs Karpenter.
- [ ] StatefulSet guarantees; when a Deployment is wrong.
- [ ] Service → EndpointSlice → dataplane; Ingress vs Gateway API.
- [ ] PodDisruptionBudgets during upgrades, and how one blocks a drain.
- [ ] RBAC and default-deny NetworkPolicy.
- [ ] Helm vs Kustomize; what Argo CD reconciles.
- [ ] Pseudo-code an operator for a `ModelDeployment` resource.

## Kubernetes for ML (W14 d4–d5, `knowledge/18`)
- [ ] Device plugin vs DRA objects.
- [ ] MIG vs MPS vs time-slicing.
- [ ] Why gang scheduling; how Kueue admits a workload.
- [ ] Cohorts, borrowing, reclaim, fair sharing.
- [ ] TrainJob/JobSet vs the old PyTorchJob; LeaderWorkerSet.
- [ ] Young/Daly checkpoint interval on spot, with numbers.
- [ ] GPU Operator components and DCGM signals.
- [ ] Why not autoscale LLM servers on GPU utilisation; what instead.
- [ ] What an endpoint picker looks at.
- [ ] Cold-start budget of a 70B replica and four mitigations.
- [ ] Multi-LoRA vs merged weights.
- [ ] Five causes of "40% utilisation but nobody gets GPUs".
- [ ] Multi-tenant GPU quotas and showback.

## Serving and fine-tuning math (W10 d4, W14 d5; LoRA: roadmap G6)
- [ ] KV bytes per token for an 8B and a 70B model.
- [ ] Max concurrency of an 8B model on 80 GB at 8k context.
- [ ] Memory for a full fine-tune of 7B parameters.
- [ ] LoRA parameter count for r=16 on a 4096×4096 matrix; why B starts at zero.
- [ ] QLoRA's three tricks.
- [ ] $/1M tokens from $/GPU-hour and tokens/s.
- [ ] Continuous batching and paged KV in two sentences.

## Kafka (W13 d1–d3, `knowledge/16`, `handson/kafka`)
- [ ] Partitions, segments, sparse index, retention.
- [ ] ISR, HW, LEO, leader epoch.
- [ ] Loss cases for each acks × min ISR combination.
- [ ] Idempotent producer: mechanism and limits.
- [ ] What exactly-once covers and what it does not.
- [ ] Rebalancing; what KIP-848 changed.
- [ ] Share groups: semantics and status.
- [ ] Compaction and tombstones.
- [ ] Partition count and key choice; hot keys; adding partitions.
- [ ] Retry topics vs DLQ.
- [ ] Kafka vs Pulsar vs Kinesis vs Pub/Sub vs RabbitMQ/SQS vs Redpanda.
- [ ] Tiered storage vs diskless topics, and what is released.
- [ ] KRaft and the migration bridge release.
- [ ] How to measure and alert on lag.

## Streams and data movement (W13 d4–d5)
- [ ] Event time vs processing time, with a metric that goes wrong.
- [ ] Watermarks, allowed lateness, side outputs.
- [ ] Tumbling / sliding / session windows.
- [ ] Checkpoint barriers and exactly-once sinks.
- [ ] Lambda vs Kappa.
- [ ] Outbox + CDC end to end.
- [ ] Schema compatibility modes and deploy order.
- [ ] 100 B events/day click aggregation, with numbers.
- [ ] Real-time features and training-serving skew (roadmap G20).
- [ ] When not to use event sourcing / CQRS.

## Databases (W4 d1–d2; rest: roadmap G7)
- [ ] B-tree vs LSM: read, write and space amplification.
- [ ] Isolation levels with one anomaly each; write skew.
- [ ] MVCC and VACUUM in Postgres.
- [ ] Read an `EXPLAIN ANALYZE`.
- [ ] Composite index column order.
- [ ] Replication, failover, split brain.
- [ ] Sharding and resharding.
- [ ] DynamoDB vs Spanner; PACELC.
- [ ] ClickHouse/BigQuery vs Postgres.
- [ ] Iceberg snapshots.
- [ ] Double-entry ledger schema.
- [ ] `SKIP LOCKED` queues.

## Design breadth (W5; rest: roadmap G8)
- [ ] Distributed cache (stampede, hot keys).   - [ ] Ticket booking.
- [ ] Payments and reconciliation.              - [ ] Time-series DB and cardinality.
- [ ] Notification system.                      - [ ] Web crawler.
- [ ] OT vs CRDT.                               - [ ] Geo matching.
- [ ] Object storage and erasure coding.        - [ ] File sync.
- [ ] Video pipeline and CDN.                   - [ ] Cross-region rate limiting.
- [ ] Design Kafka (W13).                       - [ ] Design Redis/Memcached.

## ML design (W7, W8; rest: roadmap G9, G20)
- [ ] Retrieval → ranking → re-ranking funnel with a latency budget.
- [ ] Two-tower negatives and the logQ correction.
- [ ] Position bias and inverse propensity scoring.
- [ ] CTR calibration.
- [ ] Offline–online correlation.   - [ ] Cold start.   - [ ] Exploration.
- [ ] Drift detection; shadow vs canary vs A/B.
- [ ] Point-in-time joins.
- [ ] Bias/variance; GBDT vs neural nets on tabular data; class imbalance and metrics.
- [ ] Learning to rank for search.  - [ ] Real-time fraud.

## LLM platform and agents (W6, W10; rest: roadmap G14, G16)
- [ ] Gateway: quotas, routing, caching, fallback.
- [ ] Semantic-cache risks.
- [ ] Prompt versioning with eval gates.
- [ ] Guardrails and PII.
- [ ] MCP and its security model.
- [ ] Durable execution and deterministic replay.
- [ ] Agent memory tiers.
- [ ] Trajectory evals in production.
- [ ] Per-tenant cost control.
- [ ] Multi-tenant RAG ACLs.

## Reliability (W2, W11; rest: roadmap G11)
- [ ] SLIs and SLOs for an LLM API.
- [ ] Multi-window burn-rate alerts.
- [ ] Why you cannot average p99s.
- [ ] Trace-context propagation through async work.
- [ ] Metric cardinality.
- [ ] Incident roles, and your incident story.
- [ ] Blameless postmortems.
- [ ] RPO/RTO tiers; active-active vs active-passive.
- [ ] Progressive delivery and feature flags.

## Network, security, compliance (roadmap G12, G13)
- [ ] URL to page with TLS 1.3 and HTTP/2/3.
- [ ] L4 vs L7 load balancing; power of two choices.
- [ ] gRPC vs REST vs GraphQL.
- [ ] SSE vs WebSocket through proxies.
- [ ] OAuth2 / OIDC / JWT pitfalls; mTLS and mesh.
- [ ] Tenant isolation models.
- [ ] STRIDE; the lethal trifecta; indirect prompt-injection defences.
- [ ] SBOM, signing, safetensors.
- [ ] GDPR erasure across indexes and logs.
- [ ] EU AI Act dates currently in force.

## Linux, containers, cloud (roadmap G18, G19)
- [ ] Namespaces and cgroups v2.   - [ ] Overlay filesystems; image size vs cold start.
- [ ] Page cache, mmap, zero-copy. - [ ] epoll vs threads; the GIL.
- [ ] Flame graphs.                - [ ] Little's law.
- [ ] Terraform state and drift.   - [ ] GitOps pull vs push.

## Staff behaviours (W11, `principal/`; rest: roadmap G24)
- [ ] Your 40-minute past-project presentation.
- [ ] A strategy you set: diagnosis, policy, actions, outcome.
- [ ] Build vs buy with full TCO.
- [ ] Influencing a team you did not own; a disagreement you lost.
- [ ] Your first 90 days as staff on an AI platform team.
