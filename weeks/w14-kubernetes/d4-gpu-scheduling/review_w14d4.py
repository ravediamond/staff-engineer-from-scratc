"""Review: admission of distributed training jobs in an internal batch system. On Monday mornings the cluster
shows every GPU "allocated" and no job running. Find the bug, fix it, explain:

WHY:
"""


def admit(free: dict[str, int], pods: int, gpus_per_pod: int) -> bool:
    """Reserve GPUs for a job in `free` (node -> free GPUs). True if the job can start."""
    for _ in range(pods):
        node = next((n for n in sorted(free) if free[n] >= gpus_per_pod), None)
        if node is None:
            return False
        free[node] -= gpus_per_pod
    return True
