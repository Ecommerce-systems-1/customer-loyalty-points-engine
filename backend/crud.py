import sqlite3, uuid
from datetime import datetime, timezone, timedelta
from backend.loyalty_engine import calculate_tier, calculate_points_earned, calculate_max_redemption, get_next_tier_info, POINTS_EXPIRY_MONTHS

class DuplicateOrderError(Exception): pass
class InsufficientPointsError(Exception): pass
class RedemptionCapExceededError(Exception): pass

def _now(): return datetime.now(timezone.utc).isoformat()
def _expiry(): return (datetime.now(timezone.utc) + timedelta(days=30 * POINTS_EXPIRY_MONTHS)).isoformat()

def _balance(conn, customer_id):
    r = conn.execute("SELECT COALESCE(SUM(points),0) FROM point_transactions WHERE customer_id=? AND type IN ('earn','redeem') AND expires_at>?", (customer_id, _now())).fetchone()
    return int(r[0])

def earn_points(conn, customer_id, order_id, amount_spent, is_sale):
    try:
        with conn:
            row = conn.execute("SELECT tier,lifetime_points_earned FROM customers WHERE id=?", (customer_id,)).fetchone()
            if not row: raise ValueError(f"Customer {customer_id} not found")
            pts = calculate_points_earned(amount_spent, is_sale, row["tier"])
            txn_id = str(uuid.uuid4())
            conn.execute("INSERT INTO point_transactions(id,customer_id,type,points,order_id,description,is_sale_item,expires_at,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
                (txn_id, customer_id, "earn", pts, order_id, f"Purchase {order_id}", 1 if is_sale else 0, _expiry(), _now()))
            new_lifetime = row["lifetime_points_earned"] + pts
            new_tier = calculate_tier(new_lifetime)
            conn.execute("UPDATE customers SET lifetime_points_earned=?,tier=? WHERE id=?", (new_lifetime, new_tier, customer_id))
            return {"points_earned": pts, "new_balance": _balance(conn, customer_id), "new_tier": new_tier, "tier_changed": new_tier != row["tier"], "transaction_id": txn_id}
    except sqlite3.IntegrityError as e:
        if "UNIQUE" in str(e): raise DuplicateOrderError(f"Order {order_id} already earned")
        raise

def redeem_points(conn, customer_id, order_id, points_to_redeem, order_value):
    with conn:
        avail = _balance(conn, customer_id)
        if points_to_redeem > avail: raise InsufficientPointsError("Not enough points")
        if points_to_redeem > calculate_max_redemption(order_value, avail): raise RedemptionCapExceededError("Exceeds 50% cap")
        txn_id = str(uuid.uuid4())
        discount = round(points_to_redeem / 100, 2)
        conn.execute("INSERT INTO point_transactions(id,customer_id,type,points,order_id,description,is_sale_item,expires_at,created_at) VALUES(?,?,?,?,?,?,?,?,?)",
            (txn_id, customer_id, "redeem", -points_to_redeem, order_id, f"Redemption ${discount:.2f}", 0, _expiry(), _now()))
        return {"points_redeemed": points_to_redeem, "discount_applied": discount, "new_balance": _balance(conn, customer_id), "transaction_id": txn_id}

def get_balance(conn, customer_id):
    cust = conn.execute("SELECT * FROM customers WHERE id=?", (customer_id,)).fetchone()
    if not cust: return None
    next_tier, pts_to_next = get_next_tier_info(cust["tier"], cust["lifetime_points_earned"])
    txns = conn.execute("SELECT id,type,points,description,created_at FROM point_transactions WHERE customer_id=? ORDER BY created_at DESC LIMIT 20", (customer_id,)).fetchall()
    return {"customer_id": customer_id, "name": cust["name"], "tier": cust["tier"], "current_balance": _balance(conn, customer_id), "lifetime_points_earned": cust["lifetime_points_earned"], "next_tier": next_tier, "points_to_next_tier": pts_to_next, "recent_transactions": [dict(t) for t in txns]}
