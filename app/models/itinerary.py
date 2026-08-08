from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Text, Time
from sqlalchemy.orm import relationship
from app.database.base import Base

class Attraction(Base):
    __tablename__ = "attractions"
    attraction_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=True)
    description = Column(Text, nullable=True)
    entry_fee = Column(Numeric(10, 2), default=0)
    category = Column(String(50), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    image_url = Column(String(500), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    opening_hours = Column(String(100), nullable=True)
    itineraries = relationship("Itinerary", back_populates="attraction")

class Itinerary(Base):
    __tablename__ = "itineraries"
    itinerary_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    attraction_id = Column(Integer, ForeignKey("attractions.attraction_id"), nullable=True)
    day_number = Column(Integer, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    start_time = Column(Time, nullable=True)
    end_time = Column(Time, nullable=True)
    estimated_cost = Column(Numeric(10, 2), default=0)
    trip = relationship("Trip", back_populates="itinerary")
    attraction = relationship("Attraction", back_populates="itineraries")
