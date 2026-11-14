"""Review: the rollout controller of an in-house deploy tool. A release with a bad config took the whole
service down in under a minute: every old pod was removed while the new ones were still crash-looping.
Find the bug, fix it, explain:

WHY:
"""


def old_pods_to_delete(desired: int, max_unavailable: int, old: int, new_ready: int, new_unready: int) -> int:
    available = old + new_ready + new_unready
    return max(0, min(old, available - (desired - max_unavailable)))
