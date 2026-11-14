"""W14 D3: HPA formula and stabilization, rolling-update step, PDB-aware drain."""
import math


def hpa_desired(current: int, metric: float, target: float, min_replicas: int, max_replicas: int,
                tolerance: float = 0.1) -> int:
    """ceil(current * metric / target), unchanged if |metric / target - 1| <= tolerance,
    then clamped to [min_replicas, max_replicas]."""
    # TODO
    raise NotImplementedError


class Stabilizer:
    """Scale-down stabilization: remember recommendations, apply the highest of the last `window` seconds."""

    def __init__(self, window: float = 300.0):
        self.window = window
        self.history: list[tuple[float, int]] = []

    def recommend(self, now: float, desired: int) -> int:
        """Record (now, desired); forget entries older than now - window (keep those exactly at the edge);
        return the max of what remains. Scale-up is therefore immediate, scale-down delayed."""
        # TODO
        raise NotImplementedError


def rollout_step(desired: int, max_surge: int, max_unavailable: int, old: int, new_ready: int,
                 new_unready: int) -> tuple[int, int]:
    """One step of a rolling update. Old pods are all Ready. Return (create_new, delete_old) such that
    - total pods (old + new_ready + new_unready) never exceeds desired + max_surge;
    - new pods never exceed desired;
    - available pods (old + new_ready) never drop below desired - max_unavailable.
    Create as many new pods and delete as many old pods as these rules allow (deletions are computed on
    the counts BEFORE this step's creations, since new pods start unready)."""
    # TODO
    raise NotImplementedError


def drain_plan(pods_on_node: list[str], ready: dict[str, int], min_available: dict[str, int]):
    """Drain a node. pods_on_node: app name of each pod on the node, in order (all Ready).
    ready[app]: Ready pods of that app cluster-wide (including those on this node).
    min_available[app]: its PodDisruptionBudget (apps missing from the dict have no budget).
    Evict pods one by one: an eviction is allowed iff ready[app] - 1 >= min_available[app]; an allowed
    eviction lowers ready[app] by one (the replacement is not Ready yet). Do not modify the inputs.
    Return (evicted, blocked): two lists of app names in order."""
    # TODO
    raise NotImplementedError
