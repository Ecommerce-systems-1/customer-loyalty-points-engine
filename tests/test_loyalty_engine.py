import pytest
from backend.loyalty_engine import calculate_tier, calculate_points_earned, calculate_max_redemption, get_next_tier_info

def test_bronze_earns_1pt_per_dollar():
    assert calculate_points_earned(50.75, False, "Bronze") == 50
def test_sale_earns_2x():
    assert calculate_points_earned(50.0, True, "Bronze") == 100
def test_gold_earns_5x_overrides_sale():
    assert calculate_points_earned(50.0, True, "Gold") == 250
def test_silver_earns_1pt_non_sale():
    assert calculate_points_earned(75.0, False, "Silver") == 75
def test_tier_boundary_499_500():
    assert calculate_tier(499) == "Bronze"; assert calculate_tier(500) == "Silver"
def test_tier_boundary_1999_2000():
    assert calculate_tier(1999) == "Silver"; assert calculate_tier(2000) == "Gold"
def test_max_redemption_limited_by_available():
    assert calculate_max_redemption(100.0, 3000) == 3000
def test_max_redemption_capped_at_50_percent():
    assert calculate_max_redemption(100.0, 8000) == 5000
def test_next_tier_from_bronze():
    assert get_next_tier_info("Bronze", 200) == ("Silver", 300)
def test_next_tier_from_gold_is_none():
    assert get_next_tier_info("Gold", 5000) == (None, None)
