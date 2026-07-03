import sqlite3

SCHEMA = """
CREATE TABLE IF NOT EXISTS customers (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    tier TEXT NOT NULL DEFAULT 'Bronze' CHECK(tier IN ('Bronze','Silver','Gold')),
    lifetime_points_earned INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS point_transactions (
    id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL REFERENCES customers(id),
    type TEXT NOT NULL CHECK(type IN ('earn','redeem','expire')),
    points INTEGER NOT NULL,
    order_id TEXT,
    description TEXT NOT NULL,
    is_sale_item INTEGER NOT NULL DEFAULT 0,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    UNIQUE(customer_id, order_id, type)
);

CREATE INDEX IF NOT EXISTS idx_pt_customer ON point_transactions(customer_id);
CREATE INDEX IF NOT EXISTS idx_pt_expires ON point_transactions(expires_at);
"""


def get_connection(path="points.db"):
    conn = sqlite3.connect(path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA foreign_keys=ON")
    return conn


def init_db(conn):
    conn.executescript(SCHEMA)
    conn.commit()