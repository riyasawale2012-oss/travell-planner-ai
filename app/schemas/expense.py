from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from enum import Enum

class ExpenseCategory(str, Enum):
    ACCOMMODATION = "accommodation"
    FLIGHTS = "flights"
    FOOD = "food"
    ACTIVITIES = "activities"
    SHOPPING = "shopping"
    TRANSPORT = "transport"
    INSURANCE = "insurance"
    VISA = "visa"
    EMERGENCY = "emergency"
    MISCELLANEOUS = "miscellaneous"

class ExpenseBase(BaseModel):
    amount: Decimal = Field(..., gt=0)
    currency: str = "INR"
    category: ExpenseCategory
    description: Optional[str] = Field(None, max_length=255)
    expense_date: datetime
    location: Optional[str] = None

class ExpenseCreate(ExpenseBase):
    trip_id: int

class ExpenseUpdate(BaseModel):
    amount: Optional[Decimal] = None
    currency: Optional[str] = None
    category: Optional[ExpenseCategory] = None
    description: Optional[str] = None
    expense_date: Optional[datetime] = None
    location: Optional[str] = None
    receipt_url: Optional[str] = None

class ExpenseResponse(ExpenseBase):
    model_config = ConfigDict(from_attributes=True)

    expense_id: int
    trip_id: int
    receipt_url: Optional[str] = None
    created_at: datetime

class ExpenseSummary(BaseModel):
    category: ExpenseCategory
    total: Decimal
    percentage: float
    count: int

class ExpenseReport(BaseModel):
    trip_id: int
    total_spent: Decimal
    budget: Decimal
    remaining: Decimal
    categories: List[ExpenseSummary]
    daily_average: Decimal
