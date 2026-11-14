# Questions

1. How does the scheduler choose a node? Name the two phases and three plugins of each.
2. Requests vs limits: who uses each, and what happens when a container exceeds each limit?
3. The three QoS classes and the eviction order under node memory pressure.
4. Taints/tolerations vs nodeSelector/affinity vs topology spread constraints: what is each for?
5. A latency-sensitive service shows p99 spikes at 40% CPU utilisation. What do you check first?
6. Cluster Autoscaler vs Karpenter: how does each decide to add a node, and what changes for GPU pools?

## Model answers

1. Filter (feasibility): `NodeResourcesFit` (requests fit in allocatable minus requested), `TaintToleration`, `NodeAffinity`/selector, `PodTopologySpread`, volume zone and port checks. Score (preference): `NodeResourcesFit` with LeastAllocated or MostAllocated, `ImageLocality` (image already on the node), `InterPodAffinity`, `PodTopologySpread`, `NodeResourcesBalancedAllocation`. Then reserve, permit (where gang-scheduling plugins hold pods) and bind. If nothing is feasible, preemption looks for lower-priority victims.
2. Requests: the scheduler (placement) and the kubelet (cgroup CPU shares, eviction ranking). Limits: enforced by the kernel through cgroups. Over the CPU limit: throttled for the rest of the CFS period: the process slows down, tail latency rises, nothing is killed. Over the memory limit: OOM-killed, the container restarts (`OOMKilled`, exit 137). Memory is not compressible, so a memory limit is a hard wall.
3. Guaranteed (requests = limits on all containers, both resources), Burstable (something set, not Guaranteed), BestEffort (nothing set). Under node pressure the kubelet evicts first pods whose usage exceeds their requests (BestEffort always does), ranked by priority then by how far above the request; Guaranteed pods and Burstable pods within their requests go last. The kernel OOM killer follows the same idea through `oom_score_adj`.
4. Taints (node) + tolerations (pod): keep pods OFF nodes unless they opt in: dedicate GPU pools, cordon during maintenance (`NoExecute` evicts). nodeSelector/node affinity: pull a pod TOWARD nodes with given labels (GPU type, zone). Pod (anti-)affinity: place relative to other pods. Topology spread constraints: bound the imbalance of replicas across zones or nodes. A dedicated pool needs taint + toleration + selector.
5. CPU throttling: a CPU limit with a multi-threaded runtime burns its quota in a fraction of each 100 ms period and then stalls. Check `container_cpu_cfs_throttled_periods_total`. Fix: raise or remove the CPU limit (keep the request), size thread pools to the limit. Then: noisy neighbours (requests too low), GC pauses, and connection or queue limits.
6. Cluster Autoscaler works on predefined node groups: when a pod is unschedulable it simulates which group's template would fit and grows that group; it removes under-used nodes whose pods can move. Karpenter looks at the pending pods' aggregate requirements and provisions instances directly, choosing type and size (and consolidates by replacing nodes with cheaper ones). GPU pools: capacity is often simply unavailable, nodes take minutes to be useful (driver, image, weights), and consolidation must not evict long jobs: use reservations, do-not-disrupt annotations, warm pools, and scale on queue depth rather than waiting for unschedulable pods.
