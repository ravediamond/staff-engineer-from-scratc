"""Provided: a small shop database in SQLite (in memory)."""
import sqlite3

SCHEMA = """
CREATE TABLE users  (id INTEGER PRIMARY KEY, name TEXT NOT NULL, country TEXT NOT NULL);
CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER REFERENCES users(id), amount_cents INTEGER NOT NULL,
                     status TEXT NOT NULL, created_at TEXT NOT NULL);      -- status: paid | refunded | pending
CREATE TABLE events (user_id INTEGER NOT NULL, ts INTEGER NOT NULL);      -- page views, ts in seconds
"""

USERS = [(1, "ana", "FR"), (2, "bo", "FR"), (3, "cy", "DE"), (4, "di", "DE"), (5, "ed", "ES")]
ORDERS = [  # id, user_id, amount_cents, status, created_at
    (1, 1, 5000, "paid", "2026-01-03"), (2, 1, 2000, "paid", "2026-01-10"), (3, 1, 7000, "refunded", "2026-02-01"),
    (4, 2, 3000, "paid", "2026-01-05"), (5, 2, 9000, "paid", "2026-02-11"), (6, 3, 1000, "paid", "2026-01-20"),
    (7, 3, 1000, "pending", "2026-02-02"), (8, 4, 8000, "paid", "2026-02-15"), (9, 4, 4000, "paid", "2026-02-20"),
    (10, 4, 6000, "paid", "2026-03-01"), (11, None, 500, "paid", "2026-03-02"),   # guest checkout: no user
]
EVENTS = [(1, 0), (1, 600), (1, 1500), (1, 5000), (1, 5100), (2, 100), (2, 4000), (3, 50)]


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(":memory:")
    conn.executescript(SCHEMA)
    conn.executemany("INSERT INTO users VALUES (?, ?, ?)", USERS)
    conn.executemany("INSERT INTO orders VALUES (?, ?, ?, ?, ?)", ORDERS)
    conn.executemany("INSERT INTO events VALUES (?, ?)", EVENTS)
    conn.commit()
    return conn
