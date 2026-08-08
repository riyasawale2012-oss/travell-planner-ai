from sqlalchemy import Column, Integer, String, Date, DateTime, Numeric, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
import enum

class TripStatus(str, enum.Enum):
    PLANNED = "planned"
    ONGOING = "ongoing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"

class TravelStyle(str, enum.Enum):
    BACKPACKER = "backpacker"
    BUDGET = "budget"
    MODERATE = "moderate"
    LUXURY = "luxury"
    FAMILY = "family"
    ADVENTURE = "adventure"
    ROMANTIC = "romantic"

class Trip(Base):
    __tablename__ = "trips"
    trip_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    source = Column(String(100), nullable=False)
    destination = Column(String(100), nullable=False)
    destination_country = Column(String(100), nullable=True)
    is_international = Column(Boolean, default=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    duration_days = Column(Integer, nullable=False)
    total_budget = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    num_travellers = Column(Integer, default=1)
    travel_style = Column(Enum(TravelStyle), default=TravelStyle.MODERATE)
    hotel_category = Column(String(20), nullable=True)
    transport_mode = Column(String(50), nullable=True)
    status = Column(Enum(TripStatus), default=TripStatus.PLANNED)
    ai_generated = Column(Boolean, default=False)
    cover_image = Column(String(500), nullable=True)
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="trips")
    itinerary = relationship("Itinerary", back_populates="trip", cascade="all, delete-orphan")
    budget = relationship("BudgetAllocation", back_populates="trip", uselist=False, cascade="all, delete-orphan")
    expenses = relationship("Expense", back_populates="trip", cascade="all, delete-orphan")
    bookings = relationship("Booking", back_populates="trip")
    recommendations = relationship("AIRecommendation", back_populates="trip")
    packing_lists = relationship("PackingList", back_populates="trip")
    journals = relationship("TravelJournal", back_populates="trip")
