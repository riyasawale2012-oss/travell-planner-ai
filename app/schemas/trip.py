from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from enum import Enum

class TravelStyle(str, Enum):
    BACKPACKER = "backpacker"
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"
    FAMILY = "family"
    ADVENTURE = "adventure"
    ROMANTIC = "romantic"

class TripStatus(str, Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TripBase(BaseModel):
    source: str = Field(..., min_length=2, max_length=100)
    destination: str = Field(..., min_length=2, max_length=100)
    destination_country: Optional[str] = None
    is_international: bool = False
    start_date: date
    end_date: date
    total_budget: Decimal = Field(..., gt=0)
    currency: str = "INR"
    num_travellers: int = Field(default=1, ge=1)
    travel_style: TravelStyle = TravelStyle.MODERATE
    hotel_category: Optional[str] = None
    transport_mode: Optional[str] = None
    notes: Optional[str] = None

    @field_validator("end_date")
    @classmethod
    def end_date_after_start(cls, v: date, info) -> date:
        if "start_date" in info.data and v <= info.data["start_date"]:
            raise ValueError("End date must be after start date")
        return v

class TripCreate(TripBase):
    interests: Optional[List[str]] = []

class TripUpdate(BaseModel):
    source: Optional[str] = None
    destination: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    total_budget: Optional[Decimal] = None
    num_travellers: Optional[int] = None
    travel_style: Optional[TravelStyle] = None
    hotel_category: Optional[str] = None
    transport_mode: Optional[str] = None
    status: Optional[TripStatus] = None
    notes: Optional[str] = None
    cover_image: Optional[str] = None

class TripResponse(TripBase):
    model_config = ConfigDict(from_attributes=True)

    trip_id: int
    user_id: int
    duration_days: int
    status: TripStatus
    ai_generated: bool
    cover_image: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

class TripDetail(TripResponse):
    total_expenses: Decimal = Decimal("0")
    remaining_budget: Decimal = Decimal("0")
    budget_score: Optional[int] = None
    expense_breakdown: dict = {}

class TripList(BaseModel):
    trips: List[TripResponse]
    total: int
    page: int
    per_page: int

class AIPlanRequest(BaseModel):
    current_city: str
    destination: str
    is_international: bool
    start_date: date
    end_date: date
    budget: Decimal = Field(..., gt=0)
    num_travellers: int = Field(default=1, ge=1)
    travel_style: TravelStyle = TravelStyle.MODERATE
    hotel_category: Optional[str] = "3-star"
    transport_mode: Optional[str] = "flight"
    interests: List[str] = []
