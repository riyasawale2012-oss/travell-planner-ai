from sqlalchemy import Column, Integer, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class BudgetAllocation(Base):
    __tablename__ = "budget_allocations"
    budget_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False, unique=True)
    transport_budget = Column(Numeric(12, 2), default=0)
    accommodation_budget = Column(Numeric(12, 2), default=0)
    food_budget = Column(Numeric(12, 2), default=0)
    activities_budget = Column(Numeric(12, 2), default=0)
    shopping_budget = Column(Numeric(12, 2), default=0)
    insurance_budget = Column(Numeric(12, 2), default=0)
    visa_budget = Column(Numeric(12, 2), default=0)
    emergency_budget = Column(Numeric(12, 2), default=0)
    miscellaneous_budget = Column(Numeric(12, 2), default=0)
    recommended_minimum = Column(Numeric(12, 2), nullable=True)
    recommended_ideal = Column(Numeric(12, 2), nullable=True)
    recommended_luxury = Column(Numeric(12, 2), nullable=True)
    budget_score = Column(Integer, nullable=True)
    trip = relationship("Trip", back_populates="budget")
