"""W15 D3: six SQL patterns. Each function returns ONE SQL string for the schema in schema.py (SQLite)."""


def revenue_per_country() -> str:
    """Columns: country, revenue_cents, paid_orders. Only orders with status 'paid'. EVERY country that has
    users must appear (0 and 0 if it has no paid order). Order by revenue_cents DESC, country."""
    # TODO
    raise NotImplementedError


def top2_orders_per_user() -> str:
    """Columns: user_id, order_id, amount_cents. The 2 largest PAID orders of each user (ties: smaller order id
    first). Orders without a user are excluded. Order by user_id, amount_cents DESC, order_id."""
    # TODO
    raise NotImplementedError


def running_revenue() -> str:
    """Columns: created_at, amount_cents, running_cents. Paid orders in date order (then id), with the
    cumulative sum of amount_cents so far."""
    # TODO
    raise NotImplementedError


def users_without_paid_order() -> str:
    """Column: name. Users who have no order with status 'paid'. Order by name.
    Careful: orders.user_id can be NULL."""
    # TODO
    raise NotImplementedError


def sessions_per_user() -> str:
    """Columns: user_id, sessions. A user's events belong to the same session while the gap to the previous
    event of that user is at most 1800 seconds; a larger gap (or the first event) starts a new session.
    Order by user_id."""
    # TODO
    raise NotImplementedError


def recent_orders_index_and_query() -> tuple[str, str]:
    """Return (create_index_sql, query_sql).
    Query: columns id, amount_cents: the orders of user 4 with created_at >= '2026-02-01', newest first.
    Index: ONE index on orders that lets SQLite seek on the user and the date range AND answer the query
    from the index alone (a covering index). The test reads EXPLAIN QUERY PLAN."""
    # TODO
    raise NotImplementedError
