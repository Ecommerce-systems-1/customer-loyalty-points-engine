import pytest
from fastapi.testclient import TestClient
import backend.main as m
from backend.database import get_connection, init_db


@pytest.fixture
def client(tmp_path):
    db_path = str(tmp_path / "test.db")
    db = get_connection(db_path)
    init_db(db)
    from backend.crud import earn_points
    db.execute("INSERT INTO customers(id,name,email,tier,lifetime_points_earned,created_at) VALUES('C001','Test User','t@e.com','Bronze',0,'2024-01-01T00:00:00Z')")
    db.commit()
    earn_points(db, "C001", "ORD-SETUP", 1000.0, False)
    m._conn = db
    yield TestClient(m.app)
    m._conn = None
    db.close()


def test_redeem_returns_200(client):
    r = client.post("/api/redeem", json={"customer_id": "C001", "order_id": "R01", "points_to_redeem": 500, "order_value": 60.0})
    assert r.status_code == 200
    assert r.json()["discount_applied"] == 5.0


def test_redeem_over_50pct_returns_422(client):
    r = client.post("/api/redeem", json={"customer_id": "C001", "order_id": "R02", "points_to_redeem": 4000, "order_value": 30.0})
    assert r.status_code == 422


def test_balance_returns_customer(client):
    r = client.get("/api/customer/C001/balance")
    assert r.status_code == 200
    assert r.json()["customer_id"] == "C001"


def test_unknown_customer_404(client):
    r = client.get("/api/customer/NOPE/balance")
    assert r.status_code == 404