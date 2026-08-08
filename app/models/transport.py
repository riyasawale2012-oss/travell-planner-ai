from sqlalchemy import Column, Integer, String, Numeric, Text
from app.database.base import Base

class Transport(Base):
    __tablename__ = "transports"
    transport_id = Column(Integer, primary_key=True, index=True)
    transport_type = Column(String(50), nullable=False)
    provider = Column(String(100), nullable=True)
    from_city = Column(String(100), nullable=False)
    to_city = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=True)
    duration = Column(String(50), nullable=True)
    class_type = Column(String(50), nullable=True)
    amenities = Column(Text, nullable=True)
    booking_url = Column(String(500), nullable=True)
