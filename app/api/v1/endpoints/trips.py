from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.trip_service import TripService
from app.services.expense_service import ExpenseService
from app.schemas.trip import TripCreate, TripUpdate, TripResponse, TripList, TripDetail
from app.models.user import User
from decimal import Decimal

router = APIRouter()

@router.post("", response_model=TripResponse, status_code=201)
async def create_trip(trip_data: TripCreate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TripService.create(db, current_user.user_id, trip_data)

@router.get("", response_model=TripList)
async def list_trips(
    status: Optional[str] = None,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    trips, total = await TripService.get_user_trips(db, current_user.user_id, status, page, per_page)
    return {"trips": trips, "total": total, "page": page, "per_page": per_page}

@router.get("/stats")
async def get_trip_stats(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TripService.get_trip_stats(db, current_user.user_id)

@router.get("/{trip_id}", response_model=TripDetail)
async def get_trip(trip_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    trip = await TripService.get_by_id(db, trip_id, current_user.user_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    total_spent = await ExpenseService.get_total_spent(db, trip_id, current_user.user_id)
    remaining = trip.total_budget - total_spent
    return TripDetail(
        **{k: getattr(trip, k) for k in trip.__dict__ if not k.startswith("_")},
        total_expenses=total_spent, remaining_budget=remaining,
        budget_score=trip.budget.budget_score if trip.budget else None,
        expense_breakdown={},
    )

@router.put("/{trip_id}", response_model=TripResponse)
async def update_trip(trip_id: int, trip_data: TripUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await TripService.update(db, trip_id, current_user.user_id, trip_data)

@router.delete("/{trip_id}")
async def delete_trip(trip_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await TripService.delete(db, trip_id, current_user.user_id)
    return {"message": "Trip deleted successfully"}
