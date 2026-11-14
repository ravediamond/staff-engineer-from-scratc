# W14 D3: autoscaling, rolling updates, disruption budgets

Primer: `knowledge/17-kubernetes.md` §5–6.

## The one idea

Three control loops change how many pods you have. Each has one formula worth knowing by heart.

**Horizontal Pod Autoscaler.** Every 15 s:
```
desired = ceil(current_replicas × current_metric / target_metric)
```
with a **tolerance** (no change if the ratio is within 10% of 1), min/max bounds, and a
**stabilization window** for scale-down (default 300 s): the HPA applies the **highest** recommendation
of the window, so it scales up at once and down slowly. The metric can be CPU, or anything through
custom/external metrics (KEDA: queue length, Kafka lag).

**Rolling update** of a Deployment, bounded by two numbers:
- `maxSurge`: how many pods above `replicas` may exist during the rollout;
- `maxUnavailable`: how many below `replicas` may be **unavailable**.
Only **Ready** pods are available. A new version that never becomes Ready stalls the rollout with the
old pods still serving: readiness probes are the safety catch of every deploy.

**PodDisruptionBudget.** Voluntary disruptions (node drain, upgrade, autoscaler consolidation) go
through the eviction API, which refuses an eviction that would leave fewer than `minAvailable` ready
pods. It does not protect against crashes.

## Today's build (`w14d3_rollout.py`)

`hpa_desired`, `Stabilizer`, `rollout_step`, `drain_plan`.

## Staff angle

For GPU services the defaults are wrong: `maxSurge: 25%` needs spare GPUs you may not have
(`maxSurge 0, maxUnavailable 1` trades capacity for feasibility), a 70B model takes minutes to become
Ready (use a `startupProbe`, not a long liveness delay), and CPU is the wrong autoscaling metric (d5).
