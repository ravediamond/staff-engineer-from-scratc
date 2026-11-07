"""d44 Snapshot array: set(i, v), snap() -> snap_id (0, 1, ...), get(i, snap_id) -> value at that snapshot (default 0).
Memory proportional to the number of sets, not length x snaps."""
import bisect


class SnapshotArray:
    def __init__(self, length: int):
        # TODO
        raise NotImplementedError

    def set(self, index: int, val: int) -> None:
        # TODO
        raise NotImplementedError

    def snap(self) -> int:
        # TODO
        raise NotImplementedError

    def get(self, index: int, snap_id: int) -> int:
        # TODO
        raise NotImplementedError
