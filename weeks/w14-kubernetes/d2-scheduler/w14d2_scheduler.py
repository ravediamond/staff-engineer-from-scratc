"""W14 D2: scheduler filter and score, QoS classes, eviction order.

A node: {"name", "cpu", "mem" (capacity), "used_cpu", "used_mem" (sum of requests of pods already bound),
         "labels": {k: v}, "taints": [(key, value)]}          (every taint here means NoSchedule)
A pod:  {"name", "cpu", "mem" (requests), "node_selector": {k: v}, "tolerations": [(key, value)]}
"""


def filter_nodes(pod: dict, nodes: list[dict]) -> list[str]:
    """Names of the nodes (in the given order) where the pod may run:
    requests fit in what is not yet requested, every node_selector pair is in the node's labels,
    and every taint of the node appears in the pod's tolerations."""
    # TODO
    raise NotImplementedError


def score(pod: dict, node: dict, strategy: str) -> float:
    """Score in [0, 100] AFTER placing the pod on the node.
    free = mean over cpu and mem of (capacity - used - request) / capacity.
    "spread" (LeastAllocated): 100 * free.   "binpack" (MostAllocated): 100 * (1 - free)."""
    # TODO
    raise NotImplementedError


def schedule(pod: dict, nodes: list[dict], strategy: str = "spread"):
    """Filter, score, bind: pick the feasible node with the highest score (ties: smallest name), add the
    pod's requests to its used_cpu / used_mem, and return its name. No feasible node: return None
    (the pod stays Pending) and change nothing."""
    # TODO
    raise NotImplementedError


def qos_class(containers: list[dict]) -> str:
    """containers: [{"requests": {"cpu": .., "mem": ..}, "limits": {...}}], any key may be missing.
    A missing request defaults to the limit of the same resource (as Kubernetes does).
    "BestEffort": no request and no limit anywhere. "Guaranteed": every container has cpu and mem limits and
    its (defaulted) requests equal them. Otherwise "Burstable"."""
    # TODO
    raise NotImplementedError


def eviction_order(pods: list[dict]) -> list[str]:
    """Node under memory pressure. pods: [{"name", "mem_usage", "mem_request"}] (BestEffort: request 0).
    Order of eviction (names): first the pods using MORE than their request, then the others; inside each
    group, largest (usage - request) first. (The kubelet also uses pod priority between the two; ignored here.)"""
    # TODO
    raise NotImplementedError
