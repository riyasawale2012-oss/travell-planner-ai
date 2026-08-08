from sqlalchemy import Column, Integer, String, Numeric, Text
from app.database.base import Base

class Hotel(Base):
    __tablename__ = "hotels"
    hotel_id = Column(Integer, primary_key=True, index=True)
    hotel_name = Column(String(100), nullable=False)
    city = Column(String(100), nullable=False)
    country = Column(String(100), nullable=True)
    address = Column(Text, nullable=True)
    category = Column(String(20), nullable=True)
    price_per_night = Column(Numeric(10, 2), nullable=True)
    rating = Column(Numeric(3, 2), nullable=True)
    amenities = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    latitude = Column(Numeric(10, 8), nullable=True)
    longitude = Column(Numeric(11, 8), nullable=True)
    booking_url = Column(String(500), nullable=True)
