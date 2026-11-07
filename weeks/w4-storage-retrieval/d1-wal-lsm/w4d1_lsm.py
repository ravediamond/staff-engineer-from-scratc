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
        # TODO
        raise NotImplementedError

    def replay(self) -> list:
        """All records in order. A last line that is not valid JSON (torn write) is ignored.
        An invalid line anywhere else raises ValueError (real corruption)."""
        # TODO
        raise NotImplementedError

    def truncate(self) -> None:
        # TODO
        raise NotImplementedError


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
        # TODO
        raise NotImplementedError

    def put(self, key: str, value) -> None:
        # TODO
        raise NotImplementedError

    def delete(self, key: str) -> None:
        # TODO
        raise NotImplementedError

    def get(self, key: str, default=None):
        # TODO
        raise NotImplementedError

    def flush(self) -> None:
        """Write the memtable as a sorted list of [key, value] to sst-<n>.json, make it the newest SSTable,
        clear the memtable, truncate the WAL. Write the file BEFORE truncating the WAL."""
        # TODO
        raise NotImplementedError
