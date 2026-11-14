"""Review: the autoscaling rule of an LLM inference service (vLLM on GPUs). Finance flagged it: the service
scaled to 16 GPUs during a launch and is still at 16 GPUs three weeks later at 5% of the traffic.
Find the bug, fix it, explain:

WHY:
"""
import math


def desired(current: int, metrics: dict, min_replicas: int = 1, max_replicas: int = 16) -> int:
    """metrics: {"gpu_util": 0..1 average over replicas, "waiting_per_replica": queued requests per replica}."""
    target_util = 0.6
    return max(min_replicas, min(max_replicas, math.ceil(current * metrics["gpu_util"] / target_util)))
