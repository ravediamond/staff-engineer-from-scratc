"""Review: LSM read path. After an update, some reads return the old value. Find the bug, fix it, explain:

WHY:
"""

TOMB = object()


def lsm_get(memtable: dict, sstables_newest_first: list, key):
    for table in [memtable, *reversed(sstables_newest_first)]:
        if key in table:
            v = table[key]
            return None if v is TOMB else v
    return None
