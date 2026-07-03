import sqlite3, uuid, random
from datetime import datetime, timezone, timedelta
from app.loyalty_engine import calculate_tier, calculate_points_earned

CUSTOMERS = [
    ("cust-001","Emma Wilson","emma@example.com",120), ("cust-002","Liam Johnson","liam@example.com",280),
    ("cust-003","Olivia Brown","olivia@example.com",50), ("cust-004","Noah Davis","noah@example.com",390),
    ("cust-005","Ava Martinez","ava@example.com",175), ("cust-006","Elijah Garcia","elijah@example.com",310),
    ("cust-007","Sophia Lee","sophia@example.com",85), ("cust-008","James White","james@example.com",450),
    ("cust-009","Isabella Harris","isabella@example.com",230), ("cust-010","Oliver Clark","oliver@example.com",60),
    ("cust-011","Charlotte Lewis","charlotte@example.com",650), ("cust-012","Benjamin Walker","benjamin@example.com",1100),
    ("cust-013","Amelia Hall","amelia@example.com",800), ("cust-014","Lucas Allen","lucas@example.com",1750),
    ("cust-015","Mia Young","mia@example.com",550), ("cust-016","Henry King","henry@example.com",1400),
    ("cust-017","Evelyn Wright","evelyn@example.com",2500), ("cust-018","Alexander Scott","alexander@example.com",4200),
    ("cust-019","Abigail Torres","abigail@example.com",3100), ("cust-020","Michael Green","michael@example.com",6800),
]

def seed(conn):
    conn.execute("DELETE FROM point_transactions"); conn.execute("DELETE FROM customers"); conn.commit()
    now = datetime.now(timezone.utc)
    for cid, name, email, target in CUSTOMERS:
        tier = calculate_tier(target)
        conn.execute("INSERT INTO customers VALUES(?,?,?,?,?,?)", (cid, name, email, tier, target, (now - timedelta(days=random.randint(200,730))).isoformat()))
        _gen_txns(conn, cid, target, now)
    conn.commit()

def _gen_txns(conn, cid, target, now):
    accumulated, order_num = 0, 1
    months_back = random.randint(6, 24)
    while accumulated < target:
        days_ago = random.randint(1, months_back * 30)
        txn_date = now - timedelta(days=days_ago)
        amount = float(random.randint(20, 200))
        is_sale = random.random() < 0.3
        pts = min(calculate_points_earned(amount, is_sale, calculate_tier(accumulated)), target - accumulated)
        if pts <= 0: break
        expires_at = (txn_date + timedelta(days=365)).isoformat()
        oid = f"ORD-{cid[-3:]}-{order_num:04d}"
        conn.execute("INSERT INTO point_transactions VALUES(?,?,?,?,?,?,?,?,?)", (str(uuid.uuid4()), cid, "earn", pts, oid, f"Purchase {oid}", 1 if is_sale else 0, expires_at, txn_date.isoformat()))
        accumulated += pts; order_num += 1
