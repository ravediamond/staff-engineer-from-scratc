"""W4 D1: write-ahead log + tiny LSM tree with recovery. Files are JSON for readability."""
import json
import os
from pathlib import Path

TOMBSTONE = "__tombstone__"


class WAL:
    def __init__(self, path):
        self.path = Path(path)
        self.path.touch(exist_ok=True)

    def append(self, record: dict) -> None:
        """One JSON object per line. Flush (and fsync) before returning."""
        with open(self.path, "a") as f:
            f.write(json.dumps(record) + "\n")
            f.flush()
            os.fsync(f.fileno())

    def replay(self) -> list:
        """All records in order. A last line that is not valid JSON (torn write) is ignored.
        An invalid line anywhere else raises ValueError (real corruption)."""
        lines = self.path.read_text().splitlines()
        out = []
        for i, line in enumerate(lines):
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                if i == len(lines) - 1:
                    break
                raise ValueError(f"corrupt WAL line {i}")
        return out

    def truncate(self) -> None:
        self.path.write_text("")


class LSM:
    def __init__(self, directory, memtable_limit: int = 4):
        self.dir = Path(directory)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.limit = memtable_limit
        self.memtable: dict = {}
        self.sstables: list = []  # list of dicts, NEWEST FIRST
        self.wal = WAL(self.dir / "wal.log")
        self._recover()

    def _sst_paths(self) -> list:
        return sorted(self.dir.glob("sst-*.json"), key=lambda p: int(p.stem.split("-")[1]))

    def _recover(self) -> None:
        """Load SSTables (newest first) and replay the WAL into the memtable."""
        for p in reversed(self._sst_paths()):
            self.sstables.append(dict(json.loads(p.read_text())))
        for rec in self.wal.replay():
            self.memtable[rec["k"]] = rec["v"]

    def put(self, key: str, value) -> None:
        self.wal.append({"k": key, "v": value})
        self.memtable[key] = value
        if len(self.memtable) >= self.limit:
            self.flush()

    def delete(self, key: str) -> None:
        self.put(key, TOMBSTONE)

    def get(self, key: str, default=None):
        for table in [self.memtable, *self.sstables]:
            if key in table:
                v = table[key]
                return default if v == TOMBSTONE else v
        return default

    def flush(self) -> None:
        """Write the memtable as a sorted list of [key, value] to sst-<n>.json, make it the newest SSTable,
        clear the memtable, truncate the WAL. Write the file BEFORE truncating the WAL."""
        if not self.memtable:
            return
        n = len(self._sst_paths())
        items = sorted(self.memtable.items())
        tmp = self.dir / f"sst-{n}.json.tmp"
        tmp.write_text(json.dumps(items))
        tmp.rename(self.dir / f"sst-{n}.json")
        self.sstables.insert(0, dict(items))
        self.memtable = {}
        self.wal.truncate()
