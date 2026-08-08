from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.budget_service import BudgetService
from app.schemas.budget import BudgetAllocationResponse, BudgetRecommendation, BudgetAllocationUpdate
from app.models.user import User
from decimal import Decimal

router = APIRouter()

@router.get("/trip/{trip_id}", response_model=BudgetAllocationResponse)
async def get_budget(trip_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    budget = await BudgetService.get_budget(db, trip_id, current_user.user_id)
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    return budget

@router.put("/trip/{trip_id}", response_model=BudgetAllocationResponse)
async def update_budget(trip_id: int, data: BudgetAllocationUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await BudgetService.update_budget(db, trip_id, current_user.user_id, data)

@router.post("/recommend")
async def get_budget_recommendation(
    destination: str, duration_days: int, num_travellers: int,
    is_international: bool = False, budget: Decimal = Decimal("10000"),
    current_user: User = Depends(get_current_user)
):
    return await BudgetService.generate_recommendation(destination, duration_days, num_travellers, is_international, budget)

@router.post("/savings-goal")
async def calculate_savings_goal(target_amount: Decimal, current_savings: Decimal, months_to_goal: int):
    return await BudgetService.calculate_savings_goal(target_amount, current_savings, months_to_goal)
