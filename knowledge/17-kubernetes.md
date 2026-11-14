# 17. Kubernetes

Week 14, days 1–3. What you must be able to say without notes, then prove with `kubectl` (`handson/k8s`).

## 1. Architecture

Control plane: **API server** (the only component that talks to **etcd**, a Raft-replicated store),
**scheduler**, **controller manager** (Deployment, ReplicaSet, Job, EndpointSlice, node lifecycle…),
cloud controller. Nodes: **kubelet** (runs pods through the container runtime, probes, reports
status), **kube-proxy** or an eBPF dataplane (Service routing), **CNI** plugin (pod networking),
**CSI** drivers (volumes).

Request path of a write: authentication → authorization (RBAC) → mutating admission → validation →
validating admission → etcd. Everything else reacts through **watch**.

## 2. The control loop

Objects have `spec` (desired) and `status` (observed). A controller reconciles: read state, compare,
act; **level-triggered** and **idempotent**. Informers (list + watch + local cache) feed a
deduplicating, rate-limited work queue. An **operator** = CRD + controller. Owner references give
garbage collection; finalizers give ordered cleanup.

`kubectl apply` → Deployment → ReplicaSet → Pods → scheduler binds → kubelet starts → Ready →
EndpointSlice → traffic.

## 3. Workload objects

| Object | Use | Remember |
|---|---|---|
| Deployment | stateless services | rolling updates via ReplicaSets, rollback |
| StatefulSet | databases, brokers | stable names and volumes per replica, ordered rollout |
| DaemonSet | one pod per node | agents: logs, monitoring, GPU drivers |
| Job / CronJob | run to completion | `completions`, `parallelism`, `backoffLimit`, indexed jobs |
| JobSet, LeaderWorkerSet | groups of pods as one unit | distributed training, multi-node inference |

Config: ConfigMap, Secret (base64, not encrypted by default: enable encryption at rest, prefer an
external secret manager). Packaging: Helm (templates + releases) vs Kustomize (overlays, no
templates). GitOps: Argo CD or Flux reconcile the cluster to Git (pull model), detect drift.

## 4. Scheduling and resources

Filter then score, then bind. **Requests** drive scheduling; **limits** are enforced by cgroups: CPU
is throttled, memory is OOM-killed. QoS: Guaranteed, Burstable, BestEffort; eviction under node
pressure starts with pods above their requests. Placement tools: nodeSelector/affinity (attract),
taints and tolerations (repel), pod anti-affinity and topology spread (distribute), PriorityClass
and preemption. Namespaces carry ResourceQuota and LimitRange.

## 5. Networking

Every pod has an IP; pods reach each other without NAT. A **Service** gives a stable virtual IP and DNS
name over the Ready pods (ClusterIP, NodePort, LoadBalancer; headless for StatefulSets). North-south
HTTP: **Ingress** (older, controller-specific annotations) or **Gateway API** (GatewayClass, Gateway,
HTTPRoute: role-oriented, the direction of travel; the Inference Extension builds on it).
**NetworkPolicy**: default-deny per namespace, then allow. A service mesh adds mTLS, retries and
traffic splitting between pods.

## 6. Health, rollout, scale

- Probes: **startup** (slow starters), **readiness** (take out of endpoints), **liveness** (restart).
- Rolling update bounded by `maxSurge` / `maxUnavailable`; only Ready pods are available.
  Blue-green and canary through Argo Rollouts/Flagger with metric analysis.
- **PodDisruptionBudget** limits voluntary evictions (drains, upgrades).
- **HPA**: `ceil(current × metric / target)`, 10% tolerance, 5-minute scale-down stabilization.
  **KEDA**: event-driven metrics and scale-to-zero. **VPA**: right-sizes requests.
  **Cluster Autoscaler** (node groups) vs **Karpenter** (direct provisioning, consolidation).
- Graceful shutdown: SIGTERM → `preStop` → `terminationGracePeriodSeconds` → SIGKILL; remove from
  endpoints before closing connections.

## 7. Security in five lines

RBAC with least privilege and one ServiceAccount per workload; Pod Security Standards (no root, no
privileged, read-only root filesystem); NetworkPolicy default-deny; secrets from a manager with
workload identity; signed images, admission policies (Kyverno, OPA Gatekeeper), SBOMs.

## 8. Debugging order

`kubectl get pods -o wide` → `describe pod` (events: `FailedScheduling`, `ImagePullBackOff`,
`OOMKilled`, probe failures) → `logs --previous` → `get events --sort-by=.lastTimestamp` →
`top pod/node` → `debug` with an ephemeral container. Pending = scheduling or quota;
CrashLoopBackOff = the app or its config; Running but no traffic = readiness or the Service selector.

## Questions

1. Why are controllers level-triggered?
<details><summary>Answer</summary>Events can be lost, duplicated or late; acting on observed state converges anyway and heals after crashes.</details>

2. A pod is OOMKilled every hour but the node has free memory. Why?
<details><summary>Answer</summary>It hits its own memory limit (cgroup), not node pressure. Raise the limit to the real peak or fix the leak.</details>

3. HPA and a GitOps tool both manage `replicas`. Symptom and fix?
<details><summary>Answer</summary>Replicas flap and the app shows permanent drift. Remove `replicas` from Git or ignore that field; one owner per field.</details>

4. Deployment vs StatefulSet for Kafka brokers?
<details><summary>Answer</summary>StatefulSet (usually through an operator such as Strimzi): each broker needs a stable identity and its own volume, and ordered, one-at-a-time restarts.</details>

5. What does a PDB not protect against?
<details><summary>Answer</summary>Involuntary disruptions: crashes, node failure, OOM. And the app's own rollout.</details>
