from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class TravelJournalBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: Optional[str] = None
    photos: Optional[List[str]] = []
    mood: Optional[str] = None
    rating: Optional[Decimal] = Field(None, ge=0, le=5)
    location: Optional[str] = None

class TravelJournalCreate(TravelJournalBase):
    trip_id: Optional[int] = None

class TravelJournalUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    photos: Optional[List[str]] = None
    mood: Optional[str] = None
    rating: Optional[Decimal] = None
    location: Optional[str] = None

class TravelJournalResponse(TravelJournalBase):
    model_config = ConfigDict(from_attributes=True)

    journal_id: int
    user_id: int
    trip_id: Optional[int] = None
    created_at: datetime
