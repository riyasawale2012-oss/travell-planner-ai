from fastapi import APIRouter, Depends
from app.auth.dependencies import get_current_user
from app.services.weather_service import WeatherService

router = APIRouter()

@router.get("/current/{city}")
async def get_weather(city: str, current_user = Depends(get_current_user)):
    weather = await WeatherService.get_current_weather(city)
    return weather

@router.get("/forecast/{city}")
async def get_forecast(city: str, current_user = Depends(get_current_user)):
    forecast = await WeatherService.get_forecast(city)
    return {"city": city, "forecast": forecast}
