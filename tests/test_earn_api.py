import pytest
from backend.crud import earn_points, get_balance, DuplicateOrderError

def test_earn_adds_points(db):
    r = earn_points(db, "C001", "ORD-001", 100.0, False)
    assert r["points_earned"] == 100 and r["new_balance"] == 100

def test_earn_triggers_tier_upgrade(db):
    earn_points(db, "C001", "ORD-001", 400.0, False)
    r = earn_points(db, "C001", "ORD-002", 101.0, False)
    assert r["new_tier"] == "Silver" and r["tier_changed"] is True

def test_atomic_earn_prevents_double_earn(db):
    earn_points(db, "C001", "ORD-001", 100.0, False)
    with pytest.raises(DuplicateOrderError):
        earn_points(db, "C001", "ORD-001", 100.0, False)
