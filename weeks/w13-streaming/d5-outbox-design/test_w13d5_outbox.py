import pytest

from w13d5_outbox import (Crash, InventoryConsumer, backward_compatible, connect, forward_compatible,
                          partitions_needed, place_order, relay_once)


def count(conn, table):
    return conn.execute(f"SELECT COUNT(*) FROM {table}").fetchone()[0]


def test_order_and_event_are_atomic():
    conn = connect()
    place_order(conn, "o1", "bolt", 3)
    assert count(conn, "orders") == 1 and count(conn, "outbox") == 1
    row = conn.execute("SELECT event_id, topic, key, published FROM outbox").fetchone()
    assert row == ("order-created:o1", "orders.v1", "o1", 0)
    with pytest.raises(Crash):
        place_order(conn, "o2", "bolt", 1, crash_midway=True)
    assert count(conn, "orders") == 1 and count(conn, "outbox") == 1, "no order without its event"
    with pytest.raises(Exception):
        place_order(conn, "o1", "bolt", 3)          # duplicate primary key
    assert count(conn, "outbox") == 1
    place_order(conn, "o3", "nut", 2)                # the connection is still usable
    assert count(conn, "orders") == 2


def test_relay_is_at_least_once_and_ordered():
    conn = connect()
    for i in range(3):
        place_order(conn, f"o{i}", "bolt", 1)
    sent = []
    publish = lambda topic, key, event_id, payload: sent.append(event_id)
    with pytest.raises(Crash):
        relay_once(conn, publish, crash_after_publish=True)
    assert sent == ["order-created:o0"]
    assert relay_once(conn, publish) == 3
    assert sent == ["order-created:o0", "order-created:o0", "order-created:o1", "order-created:o2"]
    assert relay_once(conn, publish) == 0


def test_idempotent_consumer_absorbs_duplicates():
    conn = connect()
    conn.execute("INSERT INTO stock VALUES ('bolt', 10)")
    conn.commit()
    place_order(conn, "o1", "bolt", 3)
    events = []
    publish = lambda topic, key, event_id, payload: events.append((event_id, payload))
    with pytest.raises(Crash):
        relay_once(conn, publish, crash_after_publish=True)
    relay_once(conn, publish)
    consumer = InventoryConsumer(conn)
    assert [consumer.handle(*e) for e in events] == [True, False]
    assert conn.execute("SELECT qty FROM stock WHERE sku = 'bolt'").fetchone()[0] == 7


def test_schema_compatibility():
    v1 = {"order_id": {"type": "string"}, "qty": {"type": "int"}}
    add_default = {**v1, "currency": {"type": "string", "default": "EUR"}}
    add_required = {**v1, "currency": {"type": "string"}}
    retype = {"order_id": {"type": "string"}, "qty": {"type": "string"}}
    drop = {"order_id": {"type": "string"}}
    assert backward_compatible(add_default, v1) and forward_compatible(add_default, v1)
    assert not backward_compatible(add_required, v1) and forward_compatible(add_required, v1)
    assert not backward_compatible(retype, v1) and not forward_compatible(retype, v1)
    assert backward_compatible(drop, v1) and not forward_compatible(drop, v1)


def test_partitions_needed():
    assert partitions_needed(200, 10, 5) == 60
    assert partitions_needed(20, 10, 50, headroom=1.0) == 2
    assert partitions_needed(1, 10, 10) == 1
