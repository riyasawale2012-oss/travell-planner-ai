from sqlalchemy import Column, Integer, String, DateTime, Numeric, Text
from sqlalchemy.sql import func
from app.database.base import Base

class Weather(Base):
    __tablename__ = "weather"
    weather_id = Column(Integer, primary_key=True, index=True)
    city = Column(String(100), nullable=False, index=True)
    country = Column(String(100), nullable=True)
    temperature = Column(Numeric(5, 2), nullable=True)
    feels_like = Column(Numeric(5, 2), nullable=True)
    humidity = Column(Integer, nullable=True)
    description = Column(String(100), nullable=True)
    icon = Column(String(50), nullable=True)
    wind_speed = Column(Numeric(5, 2), nullable=True)
    forecast_data = Column(Text, nullable=True)
    fetched_at = Column(DateTime(timezone=True), server_default=func.now())
