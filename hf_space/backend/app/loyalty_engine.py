TIER_THRESHOLDS = {"Bronze": 0, "Silver": 500, "Gold": 2000}
POINTS_PER_DOLLAR = 1
SALE_MULTIPLIER = 2
GOLD_MULTIPLIER = 5
POINTS_TO_DOLLARS = 100
MAX_REDEMPTION_RATIO = 0.5
POINTS_EXPIRY_MONTHS = 12

def calculate_tier(lp):
    if lp >= 2000: return "Gold"
    if lp >= 500: return "Silver"
    return "Bronze"

def calculate_points_earned(amt, is_sale, tier):
    base = int(amt)
    if tier == "Gold": return base * 5
    if is_sale: return base * 2
    return base

def calculate_max_redemption(ov, avail):
    return min(avail, int(ov * 0.5 * 100))

def get_next_tier_info(tier, lp):
    if tier == "Bronze": return "Silver", 500 - lp
    if tier == "Silver": return "Gold", 2000 - lp
    return None, None
