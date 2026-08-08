from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Review(Base):
    __tablename__ = "reviews"
    review_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=True)
    destination = Column(String(100), nullable=False)
    rating = Column(Numeric(3, 2), nullable=False)
    title = Column(String(200), nullable=True)
    content = Column(Text, nullable=True)
    images = Column(Text, nullable=True)
    is_approved = Column(Boolean, default=False)
    helpful_count = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="reviews")
