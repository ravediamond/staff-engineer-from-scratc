"""W13 D1: a partition log with segments, a sparse index, retention and compaction."""
from bisect import bisect_right
from typing import NamedTuple


class Record(NamedTuple):
    offset: int
    key: str
    value: object      # None = tombstone
    ts: int            # timestamp in ms


class OffsetOutOfRange(Exception):
    pass


class Segment:
    def __init__(self, base_offset: int):
        self.base_offset = base_offset
        self.records: list[Record] = []
        self.index: list[tuple[int, int]] = []   # sparse: (offset, position in self.records)


class PartitionLog:
    def __init__(self, segment_records: int = 4, index_every: int = 2):
        self.segment_records, self.index_every = segment_records, index_every
        self.segments = [Segment(0)]
        self.next_offset = 0          # log end offset (LEO)
        self.start_offset = 0         # log start offset: moved only by retention
        self.scans = 0                # records examined by linear scans in read() (tests check the index is used)

    @property
    def log_start_offset(self) -> int:
        """Provided. Lowest offset a consumer may ask for. Retention moves it; compaction does not
        (asking for a compacted-away offset simply returns the next record that still exists)."""
        return self.start_offset

    def append(self, key: str, value, ts: int) -> int:
        """Append to the active (last) segment and return the record's offset.
        If the active segment already holds segment_records records, roll: start a new segment whose
        base_offset is the new record's offset. Add an index entry (offset, position) for every record
        whose position in its segment is a multiple of index_every."""
        seg = self.segments[-1]
        if len(seg.records) >= self.segment_records:
            seg = Segment(self.next_offset)
            self.segments.append(seg)
        pos = len(seg.records)
        if pos % self.index_every == 0:
            seg.index.append((self.next_offset, pos))
        seg.records.append(Record(self.next_offset, key, value, ts))
        self.next_offset += 1
        return self.next_offset - 1

    def read(self, offset: int, max_records: int = 10) -> list[Record]:
        """Up to max_records records with record.offset >= offset, in order.
        Raise OffsetOutOfRange if offset < log_start_offset or offset > next_offset.
        Find the segment by binary search on base_offset, the start position by binary search in that
        segment's sparse index, then scan linearly. Count every record examined in self.scans."""
        if offset < self.log_start_offset or offset > self.next_offset:
            raise OffsetOutOfRange(offset)
        out: list[Record] = []
        i = max(bisect_right([s.base_offset for s in self.segments], offset) - 1, 0)
        first = True
        for seg in self.segments[i:]:
            pos = 0
            if first:
                j = bisect_right([o for o, _ in seg.index], offset) - 1
                pos = seg.index[j][1] if j >= 0 else 0
                first = False
            for rec in seg.records[pos:]:
                self.scans += 1
                if rec.offset >= offset:
                    out.append(rec)
                    if len(out) == max_records:
                        return out
        return out

    def apply_retention(self, now: int, retention_ms: int) -> int:
        """Delete closed segments, oldest first, while the NEWEST record of the segment has
        ts < now - retention_ms. Stop at the first segment that is not expired. Never delete the active
        segment. If anything was deleted, set self.start_offset to the base_offset of the first remaining
        segment. Return the number of segments deleted."""
        deleted = 0
        while len(self.segments) > 1:
            seg = self.segments[0]
            if seg.records and max(r.ts for r in seg.records) >= now - retention_ms:
                break
            self.segments.pop(0)
            deleted += 1
        if deleted:
            self.start_offset = self.segments[0].base_offset
        return deleted

    def compact(self) -> None:
        """Log compaction on the CLOSED segments: keep a record only if it is the latest record for its key
        in the whole log (the active segment counts when deciding what is latest) and is not a tombstone.
        Offsets of kept records do not change. Rebuild each compacted segment's sparse index, and drop
        closed segments that end up empty. The active segment is left untouched."""
        latest: dict[str, int] = {}
        for seg in self.segments:
            for rec in seg.records:
                latest[rec.key] = rec.offset
        kept_segments = []
        for seg in self.segments[:-1]:
            keep = [r for r in seg.records if latest[r.key] == r.offset and r.value is not None]
            if not keep:
                continue
            seg.records = keep
            seg.index = [(r.offset, pos) for pos, r in enumerate(keep) if pos % self.index_every == 0]
            kept_segments.append(seg)
        self.segments = kept_segments + [self.segments[-1]]
