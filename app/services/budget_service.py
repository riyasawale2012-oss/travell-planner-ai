from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from typing import Optional
from decimal import Decimal
from app.models.budget import BudgetAllocation
from app.models.trip import Trip
from app.schemas.budget import BudgetRecommendation, BudgetAllocationUpdate

DESTINATION_COSTS = {
    "goa": {"domestic": {"min": 1500, "ideal": 3000, "luxury": 8000}, "intl": None},
    "manali": {"domestic": {"min": 1200, "ideal": 2500, "luxury": 6000}, "intl": None},
    "jaipur": {"domestic": {"min": 1000, "ideal": 2200, "luxury": 5500}, "intl": None},
    "kerala": {"domestic": {"min": 1400, "ideal": 2800, "luxury": 7000}, "intl": None},
    "ladakh": {"domestic": {"min": 1800, "ideal": 3500, "luxury": 9000}, "intl": None},
    "bangkok": {"domestic": None, "intl": {"min": 3500, "ideal": 6000, "luxury": 15000}},
    "dubai": {"domestic": None, "intl": {"min": 5000, "ideal": 10000, "luxury": 25000}},
    "singapore": {"domestic": None, "intl": {"min": 6000, "ideal": 12000, "luxury": 30000}},
    "paris": {"domestic": None, "intl": {"min": 8000, "ideal": 15000, "luxury": 40000}},
    "bali": {"domestic": None, "intl": {"min": 3000, "ideal": 5500, "luxury": 12000}},
}
DEFAULT_DOMESTIC = {"min": 1200, "ideal": 2500, "luxury": 6000}
DEFAULT_INTL = {"min": 4000, "ideal": 8000, "luxury": 20000}

class BudgetService:
    @staticmethod
    async def get_budget(db: AsyncSession, trip_id: int, user_id: int) -> Optional[BudgetAllocation]:
        result = await db.execute(
            select(BudgetAllocation).join(Trip).where(and_(BudgetAllocation.trip_id == trip_id, Trip.user_id == user_id))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def update_budget(db: AsyncSession, trip_id: int, user_id: int, data: BudgetAllocationUpdate) -> BudgetAllocation:
        budget = await BudgetService.get_budget(db, trip_id, user_id)
        if not budget:
            raise ValueError("Budget allocation not found")
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(budget, field, value)
        await db.commit()
        await db.refresh(budget)
        return budget

    @staticmethod
    async def generate_recommendation(destination: str, duration_days: int, num_travellers: int, is_international: bool, user_budget: Decimal) -> BudgetRecommendation:
        dest_key = destination.lower().strip()
        cost_data = DESTINATION_COSTS.get(dest_key)
        if not cost_data:
            costs = DEFAULT_INTL if is_international else DEFAULT_DOMESTIC
        else:
            costs = cost_data["intl"] if is_international else cost_data["domestic"]
            if costs is None:
                costs = DEFAULT_INTL if is_international else DEFAULT_DOMESTIC

        min_per_day, ideal_per_day, luxury_per_day = costs["min"], costs["ideal"], costs["luxury"]
        flight_cost, visa_cost, insurance_cost = 0, 0, 0
        if is_international:
            flight_cost, visa_cost, insurance_cost = 25000 * num_travellers, 5000 * num_travellers, 1500 * num_travellers

        base_min = (min_per_day * duration_days * num_travellers) + flight_cost + visa_cost + insurance_cost
        base_ideal = (ideal_per_day * duration_days * num_travellers) + flight_cost + visa_cost + insurance_cost
        base_luxury = (luxury_per_day * duration_days * num_travellers) + flight_cost + visa_cost + insurance_cost

        min_total = Decimal(str(base_min * 1.15))
        ideal_total = Decimal(str(base_ideal * 1.20))
        luxury_total = Decimal(str(base_luxury * 1.25))

        if user_budget >= ideal_total:
            score = 100
        elif user_budget >= min_total:
            ratio = float(user_budget - min_total) / float(ideal_total - min_total)
            score = int(60 + (ratio * 40))
        else:
            ratio = float(user_budget) / float(min_total)
            score = int(ratio * 60)
        score = max(0, min(100, score))

        if user_budget < min_total:
            diff = min_total - user_budget
            message = f"Recommended minimum budget is approximately ₹{min_total:,.0f} per person. Increase your budget by ₹{diff:,.0f} or reduce trip duration."
        elif user_budget < ideal_total:
            message = f"Your budget is workable but tight. Recommended ideal budget is ₹{ideal_total:,.0f} for a comfortable trip."
        else:
            message = f"Great budget! You have sufficient funds for a comfortable trip. Ideal budget is ₹{ideal_total:,.0f}."

        saving_tips = [
            "Book flights 2-3 months in advance for better deals",
            "Use public transport instead of taxis",
            "Eat at local restaurants rather than tourist spots",
            "Travel during shoulder season for lower prices",
            "Use budget booking platforms and compare prices",
        ]

        alternatives = []
        if is_international:
            alternatives = ["Vietnam", "Cambodia", "Sri Lanka"] if not any(x in dest_key for x in ["dubai", "paris", "singapore"]) else (
                ["Bahrain", "Qatar", "Oman"] if "dubai" in dest_key else
                ["Prague", "Budapest", "Lisbon"] if "paris" in dest_key else
                ["Kuala Lumpur", "Bangkok", "Ho Chi Minh City"]
            )
        else:
            alternatives = ["Rishikesh", "Pushkar", "Hampi"] if not any(x in dest_key for x in ["goa", "manali"]) else (
                ["Gokarna", "Varkala", "Pondicherry"] if "goa" in dest_key else
                ["Kasol", "Tirthan Valley", "McLeod Ganj"]
            )

        breakdown = {
            "accommodation": float(ideal_total * Decimal("0.30")),
            "food": float(ideal_total * Decimal("0.20")),
            "transport": float(ideal_total * Decimal("0.20")),
            "activities": float(ideal_total * Decimal("0.15")),
            "shopping": float(ideal_total * Decimal("0.05")),
            "emergency": float(ideal_total * Decimal("0.05")),
            "miscellaneous": float(ideal_total * Decimal("0.05")),
        }
        if is_international:
            breakdown.update({"flights": float(flight_cost), "visa": float(visa_cost), "insurance": float(insurance_cost)})

        return BudgetRecommendation(
            destination=destination, duration_days=duration_days, num_travellers=num_travellers,
            is_international=is_international, user_budget=user_budget,
            recommended_minimum=min_total, recommended_ideal=ideal_total, recommended_luxury=luxury_total,
            budget_score=score, message=message, saving_tips=saving_tips,
            alternative_destinations=alternatives, breakdown=breakdown,
        )

    @staticmethod
    async def calculate_savings_goal(target_amount: Decimal, current_savings: Decimal, months_to_goal: int) -> dict:
        remaining = target_amount - current_savings
        monthly_needed = Decimal("0") if remaining <= 0 else remaining / Decimal(str(months_to_goal))
        progress = float(current_savings / target_amount * 100) if target_amount > 0 else 0
        return {
            "target_amount": target_amount, "current_savings": current_savings,
            "remaining": remaining, "monthly_savings_needed": monthly_needed,
            "months_to_goal": months_to_goal, "progress_percentage": round(progress, 2),
        }
