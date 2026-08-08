from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
import enum

class ExpenseCategory(str, enum.Enum):
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

class Expense(Base):
    __tablename__ = "expenses"
    expense_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    category = Column(Enum(ExpenseCategory), nullable=False)
    description = Column(String(255), nullable=True)
    receipt_url = Column(String(500), nullable=True)
    expense_date = Column(DateTime(timezone=True), nullable=False)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    trip = relationship("Trip", back_populates="expenses")
