from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from decimal import Decimal

class BudgetAllocationBase(BaseModel):
    transport_budget: Decimal = Decimal("0")
    accommodation_budget: Decimal = Decimal("0")
    food_budget: Decimal = Decimal("0")
    activities_budget: Decimal = Decimal("0")
    shopping_budget: Decimal = Decimal("0")
    insurance_budget: Decimal = Decimal("0")
    visa_budget: Decimal = Decimal("0")
    emergency_budget: Decimal = Decimal("0")
    miscellaneous_budget: Decimal = Decimal("0")

class BudgetAllocationCreate(BudgetAllocationBase):
    trip_id: int

class BudgetAllocationResponse(BudgetAllocationBase):
    model_config = ConfigDict(from_attributes=True)

    budget_id: int
    trip_id: int
    recommended_minimum: Optional[Decimal] = None
    recommended_ideal: Optional[Decimal] = None
    recommended_luxury: Optional[Decimal] = None
    budget_score: Optional[int] = None

class BudgetRecommendation(BaseModel):
    destination: str
    duration_days: int
    num_travellers: int
    is_international: bool
    user_budget: Decimal
    recommended_minimum: Decimal
    recommended_ideal: Decimal
    recommended_luxury: Decimal
    budget_score: int
    message: str
    saving_tips: List[str] = []
    alternative_destinations: List[str] = []
    breakdown: dict = {}

class BudgetAllocationUpdate(BaseModel):
    transport_budget: Optional[Decimal] = None
    accommodation_budget: Optional[Decimal] = None
    food_budget: Optional[Decimal] = None
    activities_budget: Optional[Decimal] = None
    shopping_budget: Optional[Decimal] = None
    insurance_budget: Optional[Decimal] = None
    visa_budget: Optional[Decimal] = None
    emergency_budget: Optional[Decimal] = None
    miscellaneous_budget: Optional[Decimal] = None

class SavingsGoal(BaseModel):
    target_amount: Decimal = Field(..., gt=0)
    current_savings: Decimal = Field(default=Decimal("0"), ge=0)
    monthly_savings_needed: Decimal
    months_to_goal: int
    progress_percentage: float
    predicted_completion: Optional[str] = None
