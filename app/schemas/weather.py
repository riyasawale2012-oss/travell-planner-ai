from pydantic import BaseModel
from typing import Optional
from decimal import Decimal
from datetime import datetime

class WeatherData(BaseModel):
    city: str
    country: Optional[str] = None
    temperature: Decimal
    feels_like: Decimal
    humidity: int
    description: str
    icon: str
    wind_speed: Decimal
    updated_at: datetime

class WeatherForecast(BaseModel):
    date: str
    temp_min: Decimal
    temp_max: Decimal
    description: str
    icon: str
    humidity: int
