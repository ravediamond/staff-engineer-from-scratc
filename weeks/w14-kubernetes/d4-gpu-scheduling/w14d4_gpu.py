"""W14 D4: gang placement, quota with borrowing and reclaim, device claims, checkpoint interval."""
import math


def place_gang(free: dict[str, int], pods: int, gpus_per_pod: int):
    """All-or-nothing placement of `pods` identical pods, each needing gpus_per_pod GPUs on ONE node.
    free: node -> free GPUs. Place pods one at a time on the feasible node with the LEAST free GPUs
    (best fit: keeps big holes for big jobs; ties: smallest node name), working on a COPY.
    Return the list of node names (one per pod) if all pods fit, else None. Never modify `free`."""
    # TODO
    raise NotImplementedError


class QuotaManager:
    """Kueue-style admission for ONE cohort. nominal: queue -> GPUs guaranteed to that queue.
    A workload is {"name", "queue", "gpus", "priority"}."""

    def __init__(self, nominal: dict[str, int]):
        self.nominal = dict(nominal)
        self.admitted: list[dict] = []          # in admission order

    def used(self, queue: str) -> int:
        """Provided."""
        return sum(w["gpus"] for w in self.admitted if w["queue"] == queue)

    def try_admit(self, wl: dict) -> tuple[bool, list[str]]:
        """Return (admitted, names of the workloads preempted to make room).

        total = sum of nominal quotas. free = total - GPUs of all admitted workloads.
        1. wl["gpus"] <= free: admit (inside its nominal quota or by borrowing idle quota).
        2. Otherwise, if the queue would stay within its nominal quota after admission
           (used(queue) + gpus <= nominal[queue]), RECLAIM: candidates are admitted workloads of OTHER
           queues that are currently above their nominal quota (borrowers). Preempt them in order
           (lowest priority first, then most recently admitted) until wl fits, skipping any workload
           whose removal would take its queue BELOW its nominal quota (that quota is guaranteed).
           If wl fits after that, remove the victims, admit wl, return (True, victims).
        3. Otherwise change nothing and return (False, [])."""
        # TODO
        raise NotImplementedError

    def release(self, name: str) -> None:
        """The workload finished: remove it."""
        # TODO
        raise NotImplementedError


def match_devices(devices: list[dict], count: int, min_memory_gb: float = 0, model: str | None = None):
    """DRA-style claim. devices: [{"name", "model", "memory_gb", "allocated": bool}].
    Pick `count` unallocated devices with memory_gb >= min_memory_gb and (model is None or equal),
    preferring the SMALLEST memory that satisfies the claim (ties: name). Mark them allocated and return
    their names; if fewer than `count` match, allocate nothing and return None."""
    # TODO
    raise NotImplementedError


def young_daly_interval(checkpoint_cost: float, mtbf: float) -> float:
    """sqrt(2 * checkpoint_cost * mtbf), same time unit as the inputs."""
    # TODO
    raise NotImplementedError


def wasted_fraction(interval: float, checkpoint_cost: float, mtbf: float) -> float:
    """First-order share of time lost: checkpoint_cost / interval (writing checkpoints)
    + interval / (2 * mtbf) (work redone after a failure: half an interval on average)."""
    # TODO
    raise NotImplementedError
