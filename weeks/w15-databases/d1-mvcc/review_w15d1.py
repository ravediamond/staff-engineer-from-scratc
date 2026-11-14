"""Review: visibility check of a home-made MVCC layer, "repeatable read" mode.

WHY: it asked "has the creator committed NOW?", which is read-committed behaviour: every new commit became
visible in the middle of the report. A repeatable-read snapshot must only see transactions that had
committed when the reader began: id below snapshot_next and not in snapshot_active.
"""


def visible(creator: int, reader_id: int, snapshot_active: set[int], snapshot_next: int, committed: set[int]) -> bool:
    if creator == reader_id:
        return True
    return creator in committed and creator < snapshot_next and creator not in snapshot_active
