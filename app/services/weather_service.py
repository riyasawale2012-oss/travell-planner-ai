import httpx
from typing import Optional
from app.config import settings

class WeatherService:
    BASE_URL = "https://api.openweathermap.org/data/2.5"

    @staticmethod
    async def get_current_weather(city: str) -> Optional[dict]:
        if not settings.OPENWEATHER_API_KEY:
            return WeatherService._mock_weather(city)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{WeatherService.BASE_URL}/weather", params={"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"})
            if response.status_code == 200:
                data = response.json()
                return {"city": city, "temperature": data["main"]["temp"], "feels_like": data["main"]["feels_like"], "humidity": data["main"]["humidity"], "description": data["weather"][0]["description"], "icon": data["weather"][0]["icon"], "wind_speed": data["wind"]["speed"]}
            return None

    @staticmethod
    async def get_forecast(city: str) -> Optional[list]:
        if not settings.OPENWEATHER_API_KEY:
            return WeatherService._mock_forecast(city)
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{WeatherService.BASE_URL}/forecast", params={"q": city, "appid": settings.OPENWEATHER_API_KEY, "units": "metric"})
            if response.status_code == 200:
                data = response.json()
                return [{"date": item["dt_txt"].split(" ")[0], "temp_min": item["main"]["temp_min"], "temp_max": item["main"]["temp_max"], "description": item["weather"][0]["description"], "icon": item["weather"][0]["icon"], "humidity": item["main"]["humidity"]} for item in data["list"][::8]]
            return None

    @staticmethod
    def _mock_weather(city: str) -> dict:
        return {"city": city, "temperature": 28.5, "feels_like": 30.2, "humidity": 65, "description": "scattered clouds", "icon": "03d", "wind_speed": 3.5}

    @staticmethod
    def _mock_forecast(city: str) -> list:
        return [
            {"date": "2024-08-06", "temp_min": 24, "temp_max": 31, "description": "clear sky", "icon": "01d", "humidity": 60},
            {"date": "2024-08-07", "temp_min": 23, "temp_max": 30, "description": "few clouds", "icon": "02d", "humidity": 62},
            {"date": "2024-08-08", "temp_min": 25, "temp_max": 32, "description": "scattered clouds", "icon": "03d", "humidity": 58},
            {"date": "2024-08-09", "temp_min": 24, "temp_max": 31, "description": "light rain", "icon": "10d", "humidity": 70},
            {"date": "2024-08-10", "temp_min": 23, "temp_max": 29, "description": "moderate rain", "icon": "10d", "humidity": 75},
        ]
