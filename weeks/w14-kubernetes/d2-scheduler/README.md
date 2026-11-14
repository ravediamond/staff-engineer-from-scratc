# W14 D2: the scheduler, requests and limits, QoS

Primer: `knowledge/17-kubernetes.md` §3–4.

## The one idea

The scheduler takes one unscheduled pod at a time and runs two phases over the nodes:

1. **Filter** (hard constraints): enough **unreserved** CPU/memory for the pod's **requests**; the node's
   labels match the pod's `nodeSelector`/affinity; every **taint** on the node is **tolerated** by the pod.
2. **Score** (preferences) the survivors and bind to the best. Two opposite strategies:
   - **spread** (`LeastAllocated`, the default): prefer emptier nodes: resilience, headroom;
   - **bin-pack** (`MostAllocated`): prefer fuller nodes: fewer nodes, and big GPU jobs still find a whole node.

The scheduler works with **requests**, never with real usage. **Limits** are enforced later on the node:
CPU above the limit is **throttled** (slow, not killed); memory above the limit is an **OOM kill**.

Requests and limits define the pod's **QoS class**, which decides who is evicted first when a node runs
out of memory:

| Class | Condition | Under node memory pressure |
|---|---|---|
| Guaranteed | every container: requests == limits for CPU and memory | last |
| Burstable | some request or limit set, not Guaranteed | pods using more than their request go before those within it |
| BestEffort | no requests, no limits | first |

**Taints** repel pods (`nvidia.com/gpu=present:NoSchedule` keeps web pods off GPU nodes);
**tolerations** let a pod in; a `nodeSelector` or affinity attracts it. You need both to dedicate a pool.

## Today's build (`w14d2_scheduler.py`)

`filter_nodes`, `score`, `schedule`, `qos_class`, `eviction_order`.

## Staff angle

Most "Kubernetes is flaky" reports are requests and limits: no requests (BestEffort pods evicted at
random), memory limit below real peak (OOM loops), CPU limits on latency-sensitive services
(throttling at 40% utilisation). For GPU nodes, bin-packing vs spreading is a cost decision worth
tens of thousands of euros a month.
