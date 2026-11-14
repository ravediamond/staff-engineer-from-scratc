"""W15 D4: single-leader replication from the application's point of view."""


class Session:
    """What the application remembers per user session (in a cookie or token)."""

    def __init__(self):
        self.last_write_lsn = 0      # read-your-writes
        self.last_seen_lsn = 0       # monotonic reads


class Cluster:
    def __init__(self, replicas: list[str], synchronous: bool = False):
        self.log: list[tuple[str, object]] = []                      # the primary's log; LSN = index + 1
        self.applied: dict[str, int] = {r: 0 for r in replicas}      # replica -> LSN applied
        self.synchronous = synchronous
        self.epoch = 1                                               # bumped at every failover

    def _state_at(self, lsn: int) -> dict:
        """Provided: the key-value state after applying the first `lsn` log entries."""
        state = {}
        for key, value in self.log[:lsn]:
            state[key] = value
        return state

    def write(self, session: Session, key: str, value) -> int:
        """Append to the primary's log; LSN = new log length. If the cluster is synchronous, the most advanced
        replica (ties: smallest name) applies everything up to this LSN before the write returns.
        Update the session (last_write_lsn, and last_seen_lsn = max(itself, lsn)). Return the LSN."""
        # TODO
        raise NotImplementedError

    def replicate(self, replica: str, up_to: int | None = None) -> None:
        """The replica applies the log up to `up_to` (None = everything). It never moves backwards."""
        # TODO
        raise NotImplementedError

    def read(self, session: Session, key: str) -> tuple[object, str]:
        """Return (value, served_by). Serve from a replica whose applied LSN is >=
        max(session.last_write_lsn, session.last_seen_lsn): choose the LEAST advanced replica that qualifies
        (ties: smallest name), to keep load off the freshest nodes. If none qualifies, serve from "primary".
        Set session.last_seen_lsn to the LSN of the state that was read (replica's applied LSN, or the
        primary's log length)."""
        # TODO
        raise NotImplementedError

    def failover(self) -> dict:
        """The primary is lost. Promote the most advanced replica (ties: smallest name): the log is truncated
        to its applied LSN, it is removed from `applied`, every other replica is capped at the new log
        length, and the epoch increases by one.
        Return {"new_primary": name, "lost_writes": number of log entries dropped, "epoch": new epoch}."""
        # TODO
        raise NotImplementedError
