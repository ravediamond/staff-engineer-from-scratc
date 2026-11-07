"""d44 Snapshot array: set(i, v), snap() -> snap_id (0, 1, ...), get(i, snap_id) -> value at that snapshot (default 0).
Memory proportional to the number of sets, not length x snaps."""
import bisect


class SnapshotArray:
    def __init__(self, length: int):
        self.hist = [[(-1, 0)] for _ in range(length)]  # per index: (snap_id, value)
        self.snap_id = 0

    def set(self, index: int, val: int) -> None:
        h = self.hist[index]
        if h[-1][0] == self.snap_id:
            h[-1] = (self.snap_id, val)
        else:
            h.append((self.snap_id, val))

    def snap(self) -> int:
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index: int, snap_id: int) -> int:
        h = self.hist[index]
        i = bisect.bisect_right(h, (snap_id, float("inf"))) - 1
        return h[i][1]
