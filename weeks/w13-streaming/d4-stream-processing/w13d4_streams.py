"""W13 D4: event-time tumbling-window counts with watermarks, allowed lateness, and checkpoints."""
import copy


class WindowedCounter:
    def __init__(self, n_partitions: int, window: int, max_out_of_order: int, allowed_lateness: int = 0):
        self.window, self.bound, self.lateness = window, max_out_of_order, allowed_lateness
        self.max_ts: list = [None] * n_partitions        # max event time seen per partition
        self.next_offset: list[int] = [0] * n_partitions  # next input offset expected per partition
        self.counts: dict[tuple[int, str], int] = {}      # (window start, key) -> count (live windows only)
        self.emitted: dict[tuple[int, str], int] = {}     # (window start, key) -> last count sent downstream
        self.late: list[tuple[int, int, str, int]] = []   # side output: (partition, offset, key, event_time)

    def watermark(self):
        """min over partitions of (max event time seen - max_out_of_order).
        None while any partition has seen no event (we know nothing about it yet)."""
        if any(t is None for t in self.max_ts):
            return None
        return min(self.max_ts) - self.bound

    def process(self, partition: int, offset: int, key: str, event_time: int) -> bool:
        """Handle one input record. Return False and do nothing if offset < next_offset[partition]
        (a replayed record already reflected in the state). Otherwise set next_offset = offset + 1, then:
        - window start = event_time // window * window, end = start + window;
        - "too late" is decided with the watermark BEFORE this event: if it is not None and
          end + allowed_lateness <= watermark, append (partition, offset, key, event_time) to self.late;
        - else count it;
        - finally update the partition's max event time. Return True."""
        if offset < self.next_offset[partition]:
            return False
        self.next_offset[partition] = offset + 1
        start = event_time // self.window * self.window
        wm = self.watermark()
        if wm is not None and start + self.window + self.lateness <= wm:
            self.late.append((partition, offset, key, event_time))
        else:
            self.counts[(start, key)] = self.counts.get((start, key), 0) + 1
        if self.max_ts[partition] is None or event_time > self.max_ts[partition]:
            self.max_ts[partition] = event_time
        return True

    def emit(self) -> list[tuple[int, str, int]]:
        """Results to send downstream now: (window start, key, count), sorted, for every window with
        end <= watermark whose count differs from the last count emitted for it (first firing or update).
        Then purge state (counts and emitted) of windows with end + allowed_lateness <= watermark."""
        wm = self.watermark()
        if wm is None:
            return []
        out = []
        for (start, key), count in sorted(self.counts.items()):
            if start + self.window <= wm and self.emitted.get((start, key)) != count:
                out.append((start, key, count))
                self.emitted[(start, key)] = count
        for k in [k for k in self.counts if k[0] + self.window + self.lateness <= wm]:
            del self.counts[k]
            self.emitted.pop(k, None)
        return out

    def snapshot(self) -> dict:
        """Checkpoint: a deep copy of everything needed to resume (state AND input offsets)."""
        return copy.deepcopy({"max_ts": self.max_ts, "next_offset": self.next_offset, "counts": self.counts,
                              "emitted": self.emitted, "late": self.late})

    def restore(self, snap: dict) -> None:
        """Replace the state by a deep copy of the snapshot."""
        snap = copy.deepcopy(snap)
        self.max_ts, self.next_offset = snap["max_ts"], snap["next_offset"]
        self.counts, self.emitted, self.late = snap["counts"], snap["emitted"], snap["late"]
