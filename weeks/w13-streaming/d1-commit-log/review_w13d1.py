"""Review: a "space-saving" log compactor. After the nightly compaction, consumers that restart skip records
or re-read old ones. Find the bug, fix it, explain:

WHY:
"""


def compact(records: list[tuple[int, str, object]]) -> list[tuple[int, str, object]]:
    """records: (offset, key, value) in offset order. Keep the latest record per key, drop tombstones."""
    latest = {}
    for offset, key, value in records:
        latest[key] = offset
    kept = [(o, k, v) for (o, k, v) in records if latest[k] == o and v is not None]
    return [(new_offset, k, v) for new_offset, (_, k, v) in enumerate(kept)]
