"""Review: visibility check of a home-made MVCC layer, "repeatable read" mode. A month-end report read the
same account twice inside one transaction and got two different balances. Find the bug, fix it, explain:

WHY:
"""


def visible(creator: int, reader_id: int, snapshot_active: set[int], snapshot_next: int, committed: set[int]) -> bool:
    """May the reader see a row version created by transaction `creator`?
    snapshot_active: transactions in progress when the reader began. snapshot_next: first id not yet started then."""
    if creator == reader_id:
        return True
    return creator in committed
