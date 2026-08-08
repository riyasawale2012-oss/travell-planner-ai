from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.expense_service import ExpenseService
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseResponse, ExpenseReport
from app.models.user import User
from decimal import Decimal

router = APIRouter()

@router.post("", response_model=ExpenseResponse, status_code=201)
async def create_expense(expense_data: ExpenseCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ExpenseService.create(db, expense_data)

@router.get("/trip/{trip_id}")
async def list_expenses(
    trip_id: int,
    category: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    expenses, total = await ExpenseService.get_trip_expenses(db, trip_id, current_user.user_id, category, page, per_page)
    return {"expenses": expenses, "total": total, "page": page, "per_page": per_page}

@router.get("/trip/{trip_id}/summary")
async def get_expense_summary(trip_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    from app.models.trip import Trip
    trip = await db.get(Trip, trip_id)
    if not trip or trip.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Trip not found")
    summary = await ExpenseService.get_expense_summary(db, trip_id, current_user.user_id)
    total_spent = await ExpenseService.get_total_spent(db, trip_id, current_user.user_id)
    return ExpenseReport(
        trip_id=trip_id, total_spent=total_spent, budget=trip.total_budget,
        remaining=trip.total_budget - total_spent, categories=summary,
        daily_average=total_spent / Decimal(str(trip.duration_days)) if trip.duration_days > 0 else Decimal("0"),
    )

@router.put("/{expense_id}", response_model=ExpenseResponse)
async def update_expense(expense_id: int, data: ExpenseUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await ExpenseService.update(db, expense_id, current_user.user_id, data)

@router.delete("/{expense_id}")
async def delete_expense(expense_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await ExpenseService.delete(db, expense_id, current_user.user_id)
    return {"message": "Expense deleted successfully"}
