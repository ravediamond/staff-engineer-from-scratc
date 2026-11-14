"""Review: the rollout controller of an in-house deploy tool.

WHY: it counted new pods as available as soon as they existed. Unready pods serve nothing: with a bad
release every new pod stayed unready, yet each one "allowed" another old pod to be deleted until none
was left. Availability counts Ready pods only; the readiness probe is what stops a bad rollout.
"""


def old_pods_to_delete(desired: int, max_unavailable: int, old: int, new_ready: int, new_unready: int) -> int:
    available = old + new_ready
    return max(0, min(old, available - (desired - max_unavailable)))
