"""W13 D5: transactional outbox, at-least-once relay, idempotent consumer, schema compatibility, sizing."""
import json
import math
import sqlite3


class Crash(Exception):
    pass


def connect() -> sqlite3.Connection:
    """Provided: an in-memory database with the service's tables."""
    conn = sqlite3.connect(":memory:")
    conn.executescript("""
        CREATE TABLE orders (id TEXT PRIMARY KEY, sku TEXT NOT NULL, qty INTEGER NOT NULL);
        CREATE TABLE outbox (id INTEGER PRIMARY KEY AUTOINCREMENT, event_id TEXT UNIQUE NOT NULL,
                             topic TEXT NOT NULL, key TEXT NOT NULL, payload TEXT NOT NULL,
                             published INTEGER NOT NULL DEFAULT 0);
        CREATE TABLE stock (sku TEXT PRIMARY KEY, qty INTEGER NOT NULL);
        CREATE TABLE processed (event_id TEXT PRIMARY KEY);
    """)
    conn.commit()
    return conn


def place_order(conn: sqlite3.Connection, order_id: str, sku: str, qty: int, crash_midway: bool = False) -> None:
    """ONE transaction: insert the order, then (raise Crash here if crash_midway) insert the outbox row with
    event_id = "order-created:" + order_id, topic "orders.v1", key = order_id, payload = JSON of
    {"order_id", "sku", "qty"}. Commit on success; on ANY exception roll back and re-raise."""
    # TODO
    raise NotImplementedError


def relay_once(conn: sqlite3.Connection, publish, crash_after_publish: bool = False) -> int:
    """Publish every unpublished outbox row in id order: call publish(topic, key, event_id, payload), THEN
    mark the row published and commit (one row at a time). If crash_after_publish, raise Crash right after
    the first publish, before marking. Return the number of rows published AND marked."""
    # TODO
    raise NotImplementedError


class InventoryConsumer:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def handle(self, event_id: str, payload: str) -> bool:
        """Decrease stock[sku] by qty exactly once per event_id: in ONE transaction, insert event_id into
        `processed` and update the stock. If the event was already processed, change nothing and return
        False. Return True when applied."""
        # TODO
        raise NotImplementedError


def backward_compatible(new: dict, old: dict) -> bool:
    """Can a reader using schema `new` read data written with schema `old`?
    A schema is {field: {"type": str, "default": value (optional key)}}.
    Yes iff every field present in both has the same type, and every field of `new` missing from `old`
    has a default. Fields removed in `new` are simply ignored by the reader."""
    # TODO
    raise NotImplementedError


def forward_compatible(new: dict, old: dict) -> bool:
    """Can a reader still using `old` read data written with `new`?"""
    # TODO
    raise NotImplementedError


def partitions_needed(target_mb_s: float, per_partition_mb_s: float, per_consumer_mb_s: float,
                      headroom: float = 1.5) -> int:
    """ceil(max(target / per_partition, target / per_consumer) * headroom)."""
    # TODO
    raise NotImplementedError
