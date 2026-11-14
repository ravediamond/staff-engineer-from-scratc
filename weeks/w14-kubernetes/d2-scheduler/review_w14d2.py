"""Review: a custom scheduler extension for GPU nodes. Pods start, then fail with "insufficient GPU" at
admission on the node, and jobs sit in a crash loop. Find the bug, fix it, explain:

WHY:
"""


def feasible(pod_gpus: int, nodes: list[dict]) -> list[str]:
    """nodes: [{"name", "gpus" (capacity), "used_gpus" (already requested by bound pods)}]."""
    return [n["name"] for n in nodes if pod_gpus <= n["gpus"]]
