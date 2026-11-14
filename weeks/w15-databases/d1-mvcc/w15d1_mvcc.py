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
        # TODO
        raise NotImplementedError

    def read(self, txn: Txn, key):
        """Value of the NEWEST version of key visible to txn (None if none). Record key in txn.reads."""
        # TODO
        raise NotImplementedError

    def write(self, txn: Txn, key, value) -> None:
        """Add a version [txn.id, value] (or replace txn's own uncommitted version of key).
        Before that, look at the existing versions of key created by OTHER transactions:
        - one from a transaction still active -> raise WriteConflict;
        - snapshot / serializable only: one from a committed transaction that txn cannot see (it committed
          after txn's snapshot) -> raise SerializationFailure (first committer wins).
        Record key in txn.writes."""
        # TODO
        raise NotImplementedError

    def commit(self, txn: Txn) -> None:
        """serializable only: if any key in txn.reads has a version created by ANOTHER committed transaction
        that txn's snapshot cannot see, abort txn and raise SerializationFailure (what it read is stale, so
        its writes may rest on a false premise). Otherwise move txn from active to committed."""
        # TODO
        raise NotImplementedError

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
        # TODO
        raise NotImplementedError
