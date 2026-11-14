"""Review: an outbox relay. Roughly once a month, after a relay pod restart, one order never reaches the
warehouse. Find the bug, fix it, explain:

WHY:
"""


def relay(rows: list[dict], publish, mark_published) -> None:
    """rows: unpublished outbox rows in id order. mark_published(row_id) commits the flag."""
    for row in rows:
        mark_published(row["id"])
        publish(row["topic"], row["key"], row["payload"])
