from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.ai_service import AIService
from app.services.budget_service import BudgetService
from app.schemas.trip import AIPlanRequest
from app.models.user import User

router = APIRouter()

@router.post("/plan-trip")
async def plan_trip(plan_request: AIPlanRequest, current_user: User = Depends(get_current_user)):
    itinerary = AIService.generate_itinerary(plan_request)
    budget_rec = await BudgetService.generate_recommendation(
        plan_request.destination, (plan_request.end_date - plan_request.start_date).days,
        plan_request.num_travellers, plan_request.is_international, plan_request.budget
    )
    return {"itinerary": itinerary, "budget_recommendation": budget_rec}

@router.post("/packing-list")
async def generate_packing_list(destination: str, duration: int, weather: str, activities: str, current_user: User = Depends(get_current_user)):
    activities_list = [a.strip() for a in activities.split(",")]
    packing_list = AIService.generate_packing_list(destination, duration, weather, activities_list)
    return {"destination": destination, "duration": duration, "packing_list": packing_list}
