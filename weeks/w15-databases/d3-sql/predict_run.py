"""Self-contained. Run after predict.md."""
import sqlite3

c = sqlite3.connect(":memory:")
c.executescript("""CREATE TABLE users (id INTEGER); CREATE TABLE orders (user_id INTEGER, shipped_at TEXT);
INSERT INTO users VALUES (1), (2), (3);
INSERT INTO orders VALUES (1, 'x'), (NULL, NULL), (1, NULL);""")
print("1. 10 and 6: COUNT(*) counts rows, COUNT(col) counts non-NULL values.")
n = c.execute("SELECT COUNT(*) FROM users WHERE id NOT IN (SELECT user_id FROM orders)").fetchone()[0]
print(f"2. {n} rows. `x NOT IN (..., NULL)` is never TRUE (it is NULL), so every row is filtered out. Use NOT EXISTS.")
print("3. No: for them orders.status is NULL, the WHERE removes them. Put the condition in the ON clause.")
print("4. x3: each payment row is repeated once per item. Aggregate each child table before joining.")
print("5. No: window functions are computed after WHERE. Compute it in a CTE or subquery, filter outside.")
