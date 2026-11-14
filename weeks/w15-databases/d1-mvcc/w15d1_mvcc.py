"""W15 D1: multi-version concurrency control with three isolation levels."""


class SerializationFailure(Exception):
    """The transaction must be retried from the start."""


class WriteConflict(Exception):
    """Another in-progress transaction has an uncommitted write on this key (a real database would wait)."""


class Txn:
    def __init__(self, txid: int, isolation: str, snapshot_active: set[int], snapshot_next: int):
        self.id = txid
        self.isolation = isolation                # "read_committed" | "snapshot" | "serializable"
        self.snapshot_active = snapshot_active    # transactions in progress when this one began
        self.snapshot_next = snapshot_next        # ids >= this had not started when this one began
        self.reads: set = set()
        self.writes: set = set()


class MVCCStore:
    def __init__(self):
        self.versions: dict = {}          # key -> list of [creator txid, value], oldest first
        self.next_txid = 1
        self.active: set[int] = set()
        self.committed: set[int] = set()
        self.aborted: set[int] = set()

    def begin(self, isolation: str = "snapshot") -> Txn:
        """Provided."""
        txn = Txn(self.next_txid, isolation, set(self.active), self.next_txid)
        self.active.add(txn.id)
        self.next_txid += 1
        return txn

    def _visible(self, txn: Txn, creator: int) -> bool:
        """May `txn` see a version created by transaction `creator`?
        - its own writes: yes; aborted creators: never;
        - read_committed: creator has committed (as of now);
        - snapshot / serializable: creator has committed AND had committed when txn began, i.e.
          creator < txn.snapshot_next and creator not in txn.snapshot_active."""
        if creator == txn.id:
            return True
        if creator not in self.committed:
            return False
        if txn.isolation == "read_committed":
            return True
        return creator < txn.snapshot_next and creator not in txn.snapshot_active

    def read(self, txn: Txn, key):
        """Value of the NEWEST version of key visible to txn (None if none). Record key in txn.reads."""
        txn.reads.add(key)
        for creator, value in reversed(self.versions.get(key, [])):
            if self._visible(txn, creator):
                return value
        return None

    def write(self, txn: Txn, key, value) -> None:
        """Add a version [txn.id, value] (or replace txn's own uncommitted version of key).
        Before that, look at the existing versions of key created by OTHER transactions:
        - one from a transaction still active -> raise WriteConflict;
        - snapshot / serializable only: one from a committed transaction that txn cannot see (it committed
          after txn's snapshot) -> raise SerializationFailure (first committer wins).
        Record key in txn.writes."""
        versions = self.versions.setdefault(key, [])
        for creator, _ in versions:
            if creator == txn.id:
                continue
            if creator in self.active:
                raise WriteConflict(key)
            if (txn.isolation != "read_committed" and creator in self.committed
                    and not self._visible(txn, creator)):
                raise SerializationFailure(key)
        for v in versions:
            if v[0] == txn.id:
                v[1] = value
                break
        else:
            versions.append([txn.id, value])
        txn.writes.add(key)

    def commit(self, txn: Txn) -> None:
        """serializable only: if any key in txn.reads has a version created by ANOTHER committed transaction
        that txn's snapshot cannot see, abort txn and raise SerializationFailure (what it read is stale, so
        its writes may rest on a false premise). Otherwise move txn from active to committed."""
        if txn.isolation == "serializable":
            for key in txn.reads:
                for creator, _ in self.versions.get(key, []):
                    if creator != txn.id and creator in self.committed and not self._visible(txn, creator):
                        self.abort(txn)
                        raise SerializationFailure(key)
        self.active.discard(txn.id)
        self.committed.add(txn.id)

    def abort(self, txn: Txn) -> None:
        """Provided: the transaction's versions stay in the lists until vacuum; they are never visible."""
        self.active.discard(txn.id)
        self.aborted.add(txn.id)

    def vacuum(self, open_txns: list[Txn]) -> int:
        """Remove dead versions and return how many were removed. For each key:
        - versions from aborted transactions are dead;
        - among committed versions, find the OLDEST one that is still the visible version for some
          transaction in open_txns or for a transaction that would begin now (i.e. the newest committed
          version); every committed version older than that one is dead.
        Versions from active transactions are kept."""
        removed = 0
        fresh = Txn(self.next_txid, "snapshot", set(self.active), self.next_txid)
        for key, versions in self.versions.items():
            needed = len(versions)
            for viewer in [fresh, *open_txns]:
                for i in range(len(versions) - 1, -1, -1):
                    creator = versions[i][0]
                    if creator in self.committed and self._visible(viewer, creator):
                        needed = min(needed, i)
                        break
            keep = [v for i, v in enumerate(versions)
                    if v[0] not in self.aborted and (v[0] in self.active or i >= needed)]
            removed += len(versions) - len(keep)
            self.versions[key] = keep
        return removed
