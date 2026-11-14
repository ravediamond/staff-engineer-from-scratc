"""Review: a "space-saving" log compactor.

WHY: it renumbers the surviving records 0..n-1. Offsets are the identity of a record: consumers store
"next offset to read" and replicas compare offsets. After renumbering, a committed offset points at a
different record. Compaction must leave offsets unchanged and accept gaps.
"""


def compact(records: list[tuple[int, str, object]]) -> list[tuple[int, str, object]]:
    latest = {}
    for offset, key, value in records:
        latest[key] = offset
    return [(o, k, v) for (o, k, v) in records if latest[k] == o and v is not None]
