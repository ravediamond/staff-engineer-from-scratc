# Week 14: Kubernetes, then Kubernetes for models

"Design the infrastructure to host and fine-tune LLMs on Kubernetes" is asked of anyone whose title
says ML platform or AI infrastructure. The answer has two layers: Kubernetes itself (controllers,
scheduler, autoscaling, rollouts), and what changes when the workload is a GPU job or an LLM server
(gang scheduling, quotas, autoscaling signal, cold start, cache-aware routing).

You build the mechanisms in Python first (d1–d5), then repeat the same experiments on a real cluster
on your Mac with `kind` (`handson/k8s/README.md`). Simulation gives you the invariants; only `kubectl`
gives you the vocabulary an interviewer listens for. Do both.

Primers: `knowledge/17-kubernetes.md`, `knowledge/18-ml-platform-on-kubernetes.md`.

| Day | Lab | Review bug |
|---|---|---|
| d1 | control loop: API store, level-triggered ReplicaSet reconcile, work queue | reacts to event deltas (edge-triggered) |
| d2 | scheduler: filter, score (spread vs bin-pack), taints, QoS classes, eviction order | fit check against capacity, not free |
| d3 | autoscaling and rollouts: HPA formula + stabilization, maxSurge/maxUnavailable, PDB drain | unready pods counted as available |
| d4 | GPU scheduling: gang placement, quotas with borrowing and reclaim, device claims, checkpoint interval | gang reserved pod by pod |
| d5 | LLM serving: KV math, cold start, cache-aware routing, autoscaling signal + **design #8** | autoscaling on GPU utilisation |
