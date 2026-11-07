"""W11 D4: resumable versioned backfill, verification, and a gated migration state machine.
Stores are dicts key -> (version, value)."""

PHASES = ["dual_write", "backfill", "verify", "cutover_reads", "stop_old_writes", "cleanup"]


def backfill(old: dict, new: dict, batch: int, checkpoint=None):
    """Copy up to `batch` keys from old into new, in sorted key order, starting AFTER `checkpoint` (None = start).
    Never overwrite a newer or equal version already in new. Return the last key processed, or None when done
    (no keys left after checkpoint)."""
    # TODO
    raise NotImplementedError


def verify(old: dict, new: dict) -> tuple:
    """Mismatch = key missing from new, or new has a LOWER version than old, or same version with a different value.
    (new may be ahead thanks to dual writes.) Return (mismatches / len(old), sorted mismatching keys); (0.0, []) if old is empty."""
    # TODO
    raise NotImplementedError


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
        # TODO
        raise NotImplementedError

    def rollback(self) -> str:
        """Allowed up to and including cutover_reads: go back to dual_write. After that: MigrationError."""
        # TODO
        raise NotImplementedError

    def read_from(self) -> str:
        """'new' from cutover_reads onwards, else 'old'."""
        # TODO
        raise NotImplementedError
