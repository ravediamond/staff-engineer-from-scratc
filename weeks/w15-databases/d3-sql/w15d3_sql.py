"""W15 D3: six SQL patterns. Each function returns ONE SQL string for the schema in schema.py (SQLite)."""


def revenue_per_country() -> str:
    """Columns: country, revenue_cents, paid_orders. Only orders with status 'paid'. EVERY country that has
    users must appear (0 and 0 if it has no paid order). Order by revenue_cents DESC, country."""
    return """
        SELECT u.country,
               COALESCE(SUM(o.amount_cents), 0) AS revenue_cents,
               COUNT(o.id) AS paid_orders
        FROM users u
        LEFT JOIN orders o ON o.user_id = u.id AND o.status = 'paid'
        GROUP BY u.country
        ORDER BY revenue_cents DESC, u.country
    """


def top2_orders_per_user() -> str:
    """Columns: user_id, order_id, amount_cents. The 2 largest PAID orders of each user (ties: smaller order id
    first). Orders without a user are excluded. Order by user_id, amount_cents DESC, order_id."""
    return """
        WITH ranked AS (
            SELECT user_id, id AS order_id, amount_cents,
                   ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY amount_cents DESC, id) AS rn
            FROM orders
            WHERE status = 'paid' AND user_id IS NOT NULL
        )
        SELECT user_id, order_id, amount_cents FROM ranked WHERE rn <= 2
        ORDER BY user_id, amount_cents DESC, order_id
    """


def running_revenue() -> str:
    """Columns: created_at, amount_cents, running_cents. Paid orders in date order (then id), with the
    cumulative sum of amount_cents so far."""
    return """
        SELECT created_at, amount_cents,
               SUM(amount_cents) OVER (ORDER BY created_at, id ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS running_cents
        FROM orders
        WHERE status = 'paid'
        ORDER BY created_at, id
    """


def users_without_paid_order() -> str:
    """Column: name. Users who have no order with status 'paid'. Order by name.
    Careful: orders.user_id can be NULL."""
    return """
        SELECT u.name
        FROM users u
        WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.user_id = u.id AND o.status = 'paid')
        ORDER BY u.name
    """


def sessions_per_user() -> str:
    """Columns: user_id, sessions. A user's events belong to the same session while the gap to the previous
    event of that user is at most 1800 seconds; a larger gap (or the first event) starts a new session.
    Order by user_id."""
    return """
        WITH flagged AS (
            SELECT user_id,
                   CASE WHEN ts - LAG(ts) OVER (PARTITION BY user_id ORDER BY ts) <= 1800 THEN 0 ELSE 1 END AS new_session
            FROM events
        )
        SELECT user_id, SUM(new_session) AS sessions
        FROM flagged
        GROUP BY user_id
        ORDER BY user_id
    """


def recent_orders_index_and_query() -> tuple[str, str]:
    """Return (create_index_sql, query_sql).
    Query: columns id, amount_cents: the orders of user 4 with created_at >= '2026-02-01', newest first.
    Index: ONE index on orders that lets SQLite seek on the user and the date range AND answer the query
    from the index alone (a covering index). The test reads EXPLAIN QUERY PLAN."""
    return (
        "CREATE INDEX idx_orders_user_date ON orders (user_id, created_at, amount_cents)",
        "SELECT id, amount_cents FROM orders WHERE user_id = 4 AND created_at >= '2026-02-01' ORDER BY created_at DESC",
    )
