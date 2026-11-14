"""Review: admission of distributed training jobs in an internal batch system.

WHY: reservations were made pod by pod directly in the shared state, and a job that could not be fully
placed returned False while KEEPING the GPUs it had already reserved. Several partial jobs then held
the whole cluster and none could start. Gang admission must be all-or-nothing: plan on a copy, commit
only if every pod fits.
"""


def admit(free: dict[str, int], pods: int, gpus_per_pod: int) -> bool:
    plan = dict(free)
    for _ in range(pods):
        node = next((n for n in sorted(plan) if plan[n] >= gpus_per_pod), None)
        if node is None:
            return False
        plan[node] -= gpus_per_pod
    free.update(plan)
    return True
