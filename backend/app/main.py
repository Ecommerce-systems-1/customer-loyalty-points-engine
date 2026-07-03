import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from app.database import init_db, get_connection
from app.models import EarnRequest, EarnResponse, RedeemRequest, RedeemResponse, BalanceResponse
from app.crud import earn_points, redeem_points, get_balance, DuplicateOrderError, InsufficientPointsError, RedemptionCapExceededError

# Module-level connection for lifespan
_conn = None

def get_db():
    """Dependency that provides the database connection."""
    return _conn

@asynccontextmanager
async def lifespan(app):
    global _conn
    _conn = get_connection(os.getenv("DB_PATH", "points.db"))
    init_db(_conn)
    if os.getenv("SEED_DB", "false").lower() == "true":
        from app.seed import seed; seed(_conn)
    yield
    if _conn: _conn.close()

app = FastAPI(title="Loyalty Points Engine", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health(): return {"status": "ok"}

@app.get("/api/customers")
def api_customers(db=Depends(get_db)):
    return [dict(r) for r in db.execute("SELECT id,name,tier FROM customers ORDER BY name").fetchall()]

@app.post("/api/earn")
def api_earn(req: EarnRequest, db=Depends(get_db)):
    try: return earn_points(db, req.customer_id, req.order_id, req.amount_spent, req.is_sale)
    except DuplicateOrderError as e: raise HTTPException(409, str(e))
    except ValueError as e: raise HTTPException(404, str(e))

@app.post("/api/redeem")
def api_redeem(req: RedeemRequest, db=Depends(get_db)):
    try: return redeem_points(db, req.customer_id, req.order_id, req.points_to_redeem, req.order_value)
    except (InsufficientPointsError, RedemptionCapExceededError) as e: raise HTTPException(422, str(e))

@app.get("/api/customer/{customer_id}/balance")
def api_balance(customer_id: str, db=Depends(get_db)):
    data = get_balance(db, customer_id)
    if not data: raise HTTPException(404, f"Customer {customer_id} not found")
    return data

if os.path.exists("/app/frontend/out"):
    app.mount("/", StaticFiles(directory="/app/frontend/out", html=True), name="static")