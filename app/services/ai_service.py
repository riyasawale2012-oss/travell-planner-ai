from typing import List, Dict, Any
from datetime import date, timedelta
from decimal import Decimal
import random
from app.schemas.trip import AIPlanRequest

class AIService:
    DOMESTIC_ATTRACTIONS = {
        "goa": [
            {"name": "Baga Beach", "type": "beach", "cost": 0},
            {"name": "Dudhsagar Falls", "type": "nature", "cost": 400},
            {"name": "Fort Aguada", "type": "historical", "cost": 25},
            {"name": "Basilica of Bom Jesus", "type": "historical", "cost": 0},
            {"name": "Anjuna Flea Market", "type": "shopping", "cost": 500},
            {"name": "Scuba Diving", "type": "adventure", "cost": 3500},
            {"name": "Sunset Cruise", "type": "relaxation", "cost": 500},
        ],
        "manali": [
            {"name": "Solang Valley", "type": "adventure", "cost": 500},
            {"name": "Rohtang Pass", "type": "nature", "cost": 550},
            {"name": "Hadimba Temple", "type": "historical", "cost": 0},
            {"name": "Old Manali", "type": "culture", "cost": 0},
            {"name": "Paragliding", "type": "adventure", "cost": 2500},
            {"name": "River Rafting", "type": "adventure", "cost": 1500},
            {"name": "Vashisht Hot Springs", "type": "relaxation", "cost": 0},
        ],
        "jaipur": [
            {"name": "Amber Fort", "type": "historical", "cost": 200},
            {"name": "Hawa Mahal", "type": "historical", "cost": 50},
            {"name": "City Palace", "type": "historical", "cost": 300},
            {"name": "Jantar Mantar", "type": "historical", "cost": 50},
            {"name": "Johari Bazaar", "type": "shopping", "cost": 1000},
            {"name": "Elephant Ride", "type": "adventure", "cost": 1100},
        ],
    }
    INTL_ATTRACTIONS = {
        "bangkok": [
            {"name": "Grand Palace", "type": "historical", "cost": 500},
            {"name": "Wat Arun", "type": "historical", "cost": 100},
            {"name": "Chatuchak Market", "type": "shopping", "cost": 2000},
            {"name": "Floating Markets", "type": "culture", "cost": 800},
            {"name": "Muay Thai Match", "type": "adventure", "cost": 1500},
        ],
        "bali": [
            {"name": "Uluwatu Temple", "type": "historical", "cost": 150},
            {"name": "Tegallalang Rice Terrace", "type": "nature", "cost": 50},
            {"name": "Mount Batur Sunrise Trek", "type": "adventure", "cost": 1200},
            {"name": "Nusa Penida Day Trip", "type": "nature", "cost": 2500},
            {"name": "Ubud Monkey Forest", "type": "nature", "cost": 400},
        ],
        "dubai": [
            {"name": "Burj Khalifa", "type": "adventure", "cost": 3000},
            {"name": "Desert Safari", "type": "adventure", "cost": 4000},
            {"name": "Dubai Mall & Aquarium", "type": "shopping", "cost": 1500},
            {"name": "Palm Jumeirah", "type": "relaxation", "cost": 0},
            {"name": "Global Village", "type": "culture", "cost": 200},
        ],
    }

    @staticmethod
    def generate_itinerary(plan_request: AIPlanRequest) -> Dict[str, Any]:
        dest_key = plan_request.destination.lower().strip()
        duration = (plan_request.end_date - plan_request.start_date).days
        attractions = AIService.INTL_ATTRACTIONS.get(dest_key, AIService.INTL_ATTRACTIONS.get("bali", [])) if plan_request.is_international else AIService.DOMESTIC_ATTRACTIONS.get(dest_key, AIService.DOMESTIC_ATTRACTIONS.get("goa", []))

        itinerary = []
        for day in range(1, duration + 1):
            day_attractions = random.sample(attractions, min(3, len(attractions)))
            lunch_cost = 800 if plan_request.is_international else 500
            dinner_cost = 1200 if plan_request.is_international else 700
            day_plan = {
                "day": day,
                "date": str(plan_request.start_date + timedelta(days=day-1)),
                "title": f"Day {day}: Explore {plan_request.destination}",
                "activities": [
                    {"time": "09:00", "name": day_attractions[0]["name"], "type": day_attractions[0]["type"], "estimated_cost": day_attractions[0]["cost"]},
                    {"time": "13:00", "name": "Local Cuisine Lunch", "type": "food", "estimated_cost": lunch_cost},
                    {"time": "15:00", "name": day_attractions[1]["name"] if len(day_attractions) > 1 else "Leisure Time", "type": day_attractions[1]["type"] if len(day_attractions) > 1 else "relaxation", "estimated_cost": day_attractions[1]["cost"] if len(day_attractions) > 1 else 0},
                    {"time": "19:00", "name": "Dinner & Evening Walk", "type": "food", "estimated_cost": dinner_cost},
                ],
                "daily_budget_estimate": day_attractions[0]["cost"] + lunch_cost + (day_attractions[1]["cost"] if len(day_attractions) > 1 else 0) + dinner_cost,
            }
            itinerary.append(day_plan)

        packing_list = AIService._generate_packing_list(plan_request, duration)
        recommendations = [
            "Book accommodations in advance for better rates",
            "Carry a universal adapter for electronics",
            "Download offline maps before travel",
            "Keep digital copies of important documents",
        ]
        if plan_request.is_international:
            recommendations.extend(["Get travel insurance before departure", "Exchange some currency before arrival", "Check visa requirements thoroughly"])

        return {
            "destination": plan_request.destination, "duration_days": duration,
            "num_travellers": plan_request.num_travellers, "travel_style": plan_request.travel_style.value,
            "itinerary": itinerary, "packing_list": packing_list,
            "recommendations": recommendations,
            "estimated_total_cost": sum(day["daily_budget_estimate"] for day in itinerary),
            "generated_at": str(date.today()),
        }

    @staticmethod
    def _generate_packing_list(plan_request, duration):
        essentials = [
            {"item": "Passport/ID", "category": "documents", "essential": True},
            {"item": "Travel Insurance", "category": "documents", "essential": True},
            {"item": "Phone Charger", "category": "electronics", "essential": True},
            {"item": "Power Bank", "category": "electronics", "essential": True},
            {"item": "Toiletries Kit", "category": "toiletries", "essential": True},
            {"item": "First Aid Kit", "category": "essentials", "essential": True},
        ]
        clothing = [
            {"item": f"{min(duration + 2, 10)} T-shirts/Tops", "category": "clothing", "essential": True},
            {"item": f"{min(duration, 5)} Bottom Wear", "category": "clothing", "essential": True},
            {"item": "Comfortable Walking Shoes", "category": "clothing", "essential": True},
            {"item": "Sunglasses & Hat", "category": "clothing", "essential": False},
        ]
        if plan_request.is_international:
            essentials.extend([
                {"item": "Visa Documents", "category": "documents", "essential": True},
                {"item": "International SIM/ eSIM", "category": "electronics", "essential": False},
                {"item": "Currency/ Forex Card", "category": "documents", "essential": True},
            ])
        if "adventure" in plan_request.travel_style.value:
            clothing.extend([{"item": "Hiking Shoes", "category": "clothing", "essential": True}, {"item": "Rain Jacket", "category": "clothing", "essential": False}])
        return essentials + clothing

    @staticmethod
    def generate_packing_list(destination, duration, weather, activities):
        base_items = [
            {"item": "Underwear", "quantity": duration + 2, "category": "clothing", "essential": True},
            {"item": "Socks", "quantity": duration + 2, "category": "clothing", "essential": True},
            {"item": "T-Shirts", "quantity": min(duration + 1, 7), "category": "clothing", "essential": True},
            {"item": "Toothbrush & Toothpaste", "quantity": 1, "category": "toiletries", "essential": True},
            {"item": "Deodorant", "quantity": 1, "category": "toiletries", "essential": True},
            {"item": "Phone Charger", "quantity": 1, "category": "electronics", "essential": True},
            {"item": "ID/Passport", "quantity": 1, "category": "documents", "essential": True},
        ]
        if "cold" in weather.lower() or "winter" in weather.lower():
            base_items.extend([{"item": "Jacket/Coat", "quantity": 1, "category": "clothing", "essential": True}, {"item": "Warm Socks", "quantity": 3, "category": "clothing", "essential": True}, {"item": "Gloves", "quantity": 1, "category": "clothing", "essential": False}])
        elif "rain" in weather.lower() or "monsoon" in weather.lower():
            base_items.extend([{"item": "Umbrella/Raincoat", "quantity": 1, "category": "essentials", "essential": True}, {"item": "Waterproof Bag", "quantity": 1, "category": "essentials", "essential": False}])
        if "beach" in activities or "swimming" in activities:
            base_items.extend([{"item": "Swimwear", "quantity": 2, "category": "clothing", "essential": True}, {"item": "Sunscreen", "quantity": 1, "category": "toiletries", "essential": True}, {"item": "Beach Towel", "quantity": 1, "category": "essentials", "essential": True}])
        if "hiking" in activities or "trekking" in activities:
            base_items.extend([{"item": "Hiking Boots", "quantity": 1, "category": "clothing", "essential": True}, {"item": "Backpack", "quantity": 1, "category": "essentials", "essential": True}, {"item": "Water Bottle", "quantity": 1, "category": "essentials", "essential": True}])
        return base_items
