from sqlalchemy import Column, Integer, String, DateTime, Numeric, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base
import enum

class BookingType(str, enum.Enum):
    FLIGHT = "flight"
    HOTEL = "hotel"
    TRAIN = "train"
    BUS = "bus"
    CAR = "car"

class BookingStatus(str, enum.Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"

class Booking(Base):
    __tablename__ = "bookings"
    booking_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=True)
    booking_type = Column(Enum(BookingType), nullable=False)
    provider = Column(String(100), nullable=True)
    provider_booking_id = Column(String(100), nullable=True)
    from_location = Column(String(100), nullable=True)
    to_location = Column(String(100), nullable=True)
    check_in = Column(DateTime(timezone=True), nullable=True)
    check_out = Column(DateTime(timezone=True), nullable=True)
    total_amount = Column(Numeric(12, 2), nullable=False)
    currency = Column(String(10), default="INR")
    status = Column(Enum(BookingStatus), default=BookingStatus.PENDING)
    booking_details = Column(Text, nullable=True)
    confirmation_number = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="bookings")
    trip = relationship("Trip", back_populates="bookings")
