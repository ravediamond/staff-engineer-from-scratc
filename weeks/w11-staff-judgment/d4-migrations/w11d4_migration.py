"""W11 D4: resumable versioned backfill, verification, and a gated migration state machine.
Stores are dicts key -> (version, value)."""

PHASES = ["dual_write", "backfill", "verify", "cutover_reads", "stop_old_writes", "cleanup"]


def backfill(old: dict, new: dict, batch: int, checkpoint=None):
    """Copy up to `batch` keys from old into new, in sorted key order, starting AFTER `checkpoint` (None = start).
    Never overwrite a newer or equal version already in new. Return the last key processed, or None when done
    (no keys left after checkpoint)."""
    keys = sorted(k for k in old if checkpoint is None or k > checkpoint)[:batch]
    if not keys:
        return None
    for k in keys:
        v_old = old[k]
        cur = new.get(k)
        if cur is None or v_old[0] > cur[0]:
            new[k] = v_old
    return keys[-1]


def verify(old: dict, new: dict) -> tuple:
    """Mismatch = key missing from new, or new has a LOWER version than old, or same version with a different value.
    (new may be ahead thanks to dual writes.) Return (mismatches / len(old), sorted mismatching keys); (0.0, []) if old is empty."""
    bad = []
    for k, (v, val) in old.items():
        cur = new.get(k)
        if cur is None or cur[0] < v or (cur[0] == v and cur[1] != val):
            bad.append(k)
    return (len(bad) / len(old) if old else 0.0), sorted(bad)


class MigrationError(Exception):
    pass


class Migration:
    def __init__(self, threshold: float):
        self.threshold = threshold
        self.phase = "dual_write"

    def advance(self, **evidence) -> str:
        """Move to the next phase if its precondition holds, else raise MigrationError:
           dual_write -> backfill:            always
           backfill -> verify:                evidence backfill_done is True
           verify -> cutover_reads:           evidence mismatch_rate <= threshold
           cutover_reads -> stop_old_writes:  evidence days_stable >= 7
           stop_old_writes -> cleanup:        always
        Return the new phase."""
        i = PHASES.index(self.phase)
        if i == len(PHASES) - 1:
            raise MigrationError("already done")
        nxt = PHASES[i + 1]
        if nxt == "verify" and evidence.get("backfill_done") is not True:
            raise MigrationError("backfill not complete")
        if nxt == "cutover_reads":
            rate = evidence.get("mismatch_rate")
            if rate is None or rate > self.threshold:
                raise MigrationError(f"verification failed: {rate}")
        if nxt == "stop_old_writes" and evidence.get("days_stable", 0) < 7:
            raise MigrationError("not stable long enough")
        self.phase = nxt
        return nxt

    def rollback(self) -> str:
        """Allowed up to and including cutover_reads: go back to dual_write. After that: MigrationError."""
        if PHASES.index(self.phase) > PHASES.index("cutover_reads"):
            raise MigrationError("old store no longer receives writes")
        self.phase = "dual_write"
        return self.phase

    def read_from(self) -> str:
        """'new' from cutover_reads onwards, else 'old'."""
        return "new" if PHASES.index(self.phase) >= PHASES.index("cutover_reads") else "old"
