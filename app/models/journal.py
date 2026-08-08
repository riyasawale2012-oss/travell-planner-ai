from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class TravelJournal(Base):
    __tablename__ = "travel_journals"
    journal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=True)
    title = Column(String(200), nullable=False)
    content = Column(Text, nullable=True)
    photos = Column(Text, nullable=True)
    mood = Column(String(50), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    location = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="journals")
    trip = relationship("Trip", back_populates="journals")
