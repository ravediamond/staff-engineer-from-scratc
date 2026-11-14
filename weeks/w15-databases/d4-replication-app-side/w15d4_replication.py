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
        self.log.append((key, value))
        lsn = len(self.log)
        if self.synchronous and self.applied:
            best = min(self.applied, key=lambda r: (-self.applied[r], r))
            self.applied[best] = lsn
        session.last_write_lsn = lsn
        session.last_seen_lsn = max(session.last_seen_lsn, lsn)
        return lsn

    def replicate(self, replica: str, up_to: int | None = None) -> None:
        """The replica applies the log up to `up_to` (None = everything). It never moves backwards."""
        target = len(self.log) if up_to is None else min(up_to, len(self.log))
        self.applied[replica] = max(self.applied[replica], target)

    def read(self, session: Session, key: str) -> tuple[object, str]:
        """Return (value, served_by). Serve from a replica whose applied LSN is >=
        max(session.last_write_lsn, session.last_seen_lsn): choose the LEAST advanced replica that qualifies
        (ties: smallest name), to keep load off the freshest nodes. If none qualifies, serve from "primary".
        Set session.last_seen_lsn to the LSN of the state that was read (replica's applied LSN, or the
        primary's log length)."""
        need = max(session.last_write_lsn, session.last_seen_lsn)
        ok = [r for r in self.applied if self.applied[r] >= need]
        if ok:
            who = min(ok, key=lambda r: (self.applied[r], r))
            lsn = self.applied[who]
        else:
            who, lsn = "primary", len(self.log)
        session.last_seen_lsn = lsn
        return self._state_at(lsn).get(key), who

    def failover(self) -> dict:
        """The primary is lost. Promote the most advanced replica (ties: smallest name): the log is truncated
        to its applied LSN, it is removed from `applied`, every other replica is capped at the new log
        length, and the epoch increases by one.
        Return {"new_primary": name, "lost_writes": number of log entries dropped, "epoch": new epoch}."""
        best = min(self.applied, key=lambda r: (-self.applied[r], r))
        keep = self.applied.pop(best)
        lost = len(self.log) - keep
        del self.log[keep:]
        for r in self.applied:
            self.applied[r] = min(self.applied[r], keep)
        self.epoch += 1
        return {"new_primary": best, "lost_writes": lost, "epoch": self.epoch}
