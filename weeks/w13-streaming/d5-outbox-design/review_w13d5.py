"""Review: an outbox relay.

WHY: it marked the row as published BEFORE publishing. A crash between the two leaves a row flagged as
sent that was never sent: the event is lost and nothing will retry it (at-most-once). Publish first,
mark after: a crash then causes a duplicate, which idempotent consumers absorb (at-least-once).
"""


def relay(rows: list[dict], publish, mark_published) -> None:
    for row in rows:
        publish(row["topic"], row["key"], row["payload"])
        mark_published(row["id"])
