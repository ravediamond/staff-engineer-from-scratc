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
        # TODO
        raise NotImplementedError

    def process(self, partition: int, offset: int, key: str, event_time: int) -> bool:
        """Handle one input record. Return False and do nothing if offset < next_offset[partition]
        (a replayed record already reflected in the state). Otherwise set next_offset = offset + 1, then:
        - window start = event_time // window * window, end = start + window;
        - "too late" is decided with the watermark BEFORE this event: if it is not None and
          end + allowed_lateness <= watermark, append (partition, offset, key, event_time) to self.late;
        - else count it;
        - finally update the partition's max event time. Return True."""
        # TODO
        raise NotImplementedError

    def emit(self) -> list[tuple[int, str, int]]:
        """Results to send downstream now: (window start, key, count), sorted, for every window with
        end <= watermark whose count differs from the last count emitted for it (first firing or update).
        Then purge state (counts and emitted) of windows with end + allowed_lateness <= watermark."""
        # TODO
        raise NotImplementedError

    def snapshot(self) -> dict:
        """Checkpoint: a deep copy of everything needed to resume (state AND input offsets)."""
        # TODO
        raise NotImplementedError

    def restore(self, snap: dict) -> None:
        """Replace the state by a deep copy of the snapshot."""
        # TODO
        raise NotImplementedError
