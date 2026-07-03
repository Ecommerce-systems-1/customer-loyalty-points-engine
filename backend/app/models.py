from pydantic import BaseModel, Field
class EarnRequest(BaseModel):
    customer_id: str; order_id: str
    amount_spent: float = Field(gt=0); is_sale: bool = False
class EarnResponse(BaseModel):
    points_earned: int; new_balance: int; new_tier: str; tier_changed: bool; transaction_id: str
class RedeemRequest(BaseModel):
    customer_id: str; order_id: str
    points_to_redeem: int = Field(gt=0); order_value: float = Field(gt=0)
class RedeemResponse(BaseModel):
    points_redeemed: int; discount_applied: float; new_balance: int; transaction_id: str
class TransactionSummary(BaseModel):
    id: str; type: str; points: int; description: str; created_at: str
class BalanceResponse(BaseModel):
    customer_id: str; name: str; tier: str; current_balance: int; lifetime_points_earned: int
    next_tier: str | None; points_to_next_tier: int | None
    recent_transactions: list[TransactionSummary]
