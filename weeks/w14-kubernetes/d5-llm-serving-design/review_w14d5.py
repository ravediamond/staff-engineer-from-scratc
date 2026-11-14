"""Review: the autoscaling rule of an LLM inference service (vLLM on GPUs).

WHY: it scaled on GPU utilisation. A server with continuous batching keeps the GPU near 100% whenever it
is decoding anything, so the signal says "overloaded" at any traffic level: the service scales up to the
maximum and never down. Scale on work waiting (queue depth per replica; also KV-cache usage or TTFT).
"""
import math


def desired(current: int, metrics: dict, min_replicas: int = 1, max_replicas: int = 16) -> int:
    target_waiting = 4.0
    return max(min_replicas, min(max_replicas, math.ceil(current * metrics["waiting_per_replica"] / target_waiting)))
