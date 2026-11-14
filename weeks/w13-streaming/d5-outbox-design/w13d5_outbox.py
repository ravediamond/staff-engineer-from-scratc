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
    try:
        conn.execute("INSERT INTO orders (id, sku, qty) VALUES (?, ?, ?)", (order_id, sku, qty))
        if crash_midway:
            raise Crash()
        conn.execute("INSERT INTO outbox (event_id, topic, key, payload) VALUES (?, ?, ?, ?)",
                     (f"order-created:{order_id}", "orders.v1", order_id,
                      json.dumps({"order_id": order_id, "sku": sku, "qty": qty})))
        conn.commit()
    except BaseException:
        conn.rollback()
        raise


def relay_once(conn: sqlite3.Connection, publish, crash_after_publish: bool = False) -> int:
    """Publish every unpublished outbox row in id order: call publish(topic, key, event_id, payload), THEN
    mark the row published and commit (one row at a time). If crash_after_publish, raise Crash right after
    the first publish, before marking. Return the number of rows published AND marked."""
    rows = conn.execute("SELECT id, topic, key, event_id, payload FROM outbox WHERE published = 0 ORDER BY id").fetchall()
    done = 0
    for row_id, topic, key, event_id, payload in rows:
        publish(topic, key, event_id, payload)
        if crash_after_publish:
            raise Crash()
        conn.execute("UPDATE outbox SET published = 1 WHERE id = ?", (row_id,))
        conn.commit()
        done += 1
    return done


class InventoryConsumer:
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn

    def handle(self, event_id: str, payload: str) -> bool:
        """Decrease stock[sku] by qty exactly once per event_id: in ONE transaction, insert event_id into
        `processed` and update the stock. If the event was already processed, change nothing and return
        False. Return True when applied."""
        try:
            self.conn.execute("INSERT INTO processed (event_id) VALUES (?)", (event_id,))
        except sqlite3.IntegrityError:
            self.conn.rollback()
            return False
        event = json.loads(payload)
        self.conn.execute("UPDATE stock SET qty = qty - ? WHERE sku = ?", (event["qty"], event["sku"]))
        self.conn.commit()
        return True


def backward_compatible(new: dict, old: dict) -> bool:
    """Can a reader using schema `new` read data written with schema `old`?
    A schema is {field: {"type": str, "default": value (optional key)}}.
    Yes iff every field present in both has the same type, and every field of `new` missing from `old`
    has a default. Fields removed in `new` are simply ignored by the reader."""
    for name, spec in new.items():
        if name in old:
            if old[name]["type"] != spec["type"]:
                return False
        elif "default" not in spec:
            return False
    return True


def forward_compatible(new: dict, old: dict) -> bool:
    """Can a reader still using `old` read data written with `new`?"""
    return backward_compatible(old, new)


def partitions_needed(target_mb_s: float, per_partition_mb_s: float, per_consumer_mb_s: float,
                      headroom: float = 1.5) -> int:
    """ceil(max(target / per_partition, target / per_consumer) * headroom)."""
    return math.ceil(max(target_mb_s / per_partition_mb_s, target_mb_s / per_consumer_mb_s) * headroom)
