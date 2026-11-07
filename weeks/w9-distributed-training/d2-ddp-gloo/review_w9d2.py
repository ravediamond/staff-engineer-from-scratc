"""Review: gradient sync for a custom training loop. At 8 GPUs training diverged; at 1 GPU it was fine.
Here all_reduce is simulated: grads_per_rank[r] is rank r's local gradient. Return what each rank holds after sync.
Find the bug, fix it, explain:

WHY:
"""
import torch


def sync(grads_per_rank: list) -> list:
    total = torch.stack(grads_per_rank).sum(0)
    return [total / len(grads_per_rank) for _ in grads_per_rank]
