"""Review: a custom scheduler extension for GPU nodes.

WHY: the fit check compared the request with the node's CAPACITY, ignoring what bound pods have already
requested. Every 8-GPU node looked feasible for ever, so pods were bound to full nodes and rejected by
the kubelet. Fit = request <= capacity - already requested.
"""


def feasible(pod_gpus: int, nodes: list[dict]) -> list[str]:
    return [n["name"] for n in nodes if pod_gpus <= n["gpus"] - n["used_gpus"]]
