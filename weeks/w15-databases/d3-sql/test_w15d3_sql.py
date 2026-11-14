import schema
import w15d3_sql as q


def run(sql):
    return schema.connect().execute(sql).fetchall()


def test_revenue_per_country():
    assert run(q.revenue_per_country()) == [("DE", 19000, 4), ("FR", 19000, 4), ("ES", 0, 0)]


def test_top2_orders_per_user():
    assert run(q.top2_orders_per_user()) == [(1, 1, 5000), (1, 2, 2000), (2, 5, 9000), (2, 4, 3000),
                                             (3, 6, 1000), (4, 8, 8000), (4, 10, 6000)]


def test_running_revenue():
    rows = run(q.running_revenue())
    assert [r[2] for r in rows] == [5000, 8000, 10000, 11000, 20000, 28000, 32000, 38000, 38500]
    assert rows[0][:2] == ("2026-01-03", 5000)


def test_users_without_paid_order():
    assert run(q.users_without_paid_order()) == [("ed",)]


def test_sessions_per_user():
    assert run(q.sessions_per_user()) == [(1, 2), (2, 2), (3, 1)]


def test_index_is_used_and_covering():
    create_index, query = q.recent_orders_index_and_query()
    conn = schema.connect()
    assert conn.execute(query).fetchall() == [(10, 6000), (9, 4000), (8, 8000)]
    before = " ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + query))
    assert "SCAN" in before, "without an index SQLite scans the table"
    conn.execute(create_index)
    plan = " ".join(r[3] for r in conn.execute("EXPLAIN QUERY PLAN " + query))
    assert "SEARCH" in plan and "COVERING INDEX" in plan, plan
    assert "user_id=? AND created_at>?" in plan, f"the index must be usable for both predicates: {plan}"
    assert "TEMP B-TREE" not in plan, "the index order should also serve the ORDER BY"
    assert conn.execute(query).fetchall() == [(10, 6000), (9, 4000), (8, 8000)]
