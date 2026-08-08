from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.user_service import UserService
from app.schemas.user import UserUpdate, UserResponse, UserProfile
from app.models.user import User
from app.models.trip import Trip
from app.models.achievement import Achievement
from app.models.expense import Expense

router = APIRouter()

@router.get("/profile", response_model=UserProfile)
async def get_profile(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    trips_count_res = await db.execute(select(func.count()).where(Trip.user_id == current_user.user_id))
    total_trips = trips_count_res.scalar() or 0

    achievements_count_res = await db.execute(select(func.count()).where(Achievement.user_id == current_user.user_id))
    achievements_count = achievements_count_res.scalar() or 0

    spent_res = await db.execute(
        select(func.sum(Expense.amount)).join(Trip).where(Trip.user_id == current_user.user_id)
    )
    total_spent = float(spent_res.scalar() or 0.0)

    countries_res = await db.execute(
        select(func.count(func.distinct(Trip.destination_country))).where(Trip.user_id == current_user.user_id)
    )
    total_countries = countries_res.scalar() or 0

    return UserProfile(
        user_id=current_user.user_id,
        full_name=current_user.full_name,
        email=current_user.email,
        phone=current_user.phone,
        avatar_url=current_user.avatar_url,
        role=current_user.role,
        is_active=current_user.is_active,
        is_verified=current_user.is_verified,
        created_at=current_user.created_at,
        last_login=current_user.last_login,
        currency_preference=current_user.currency_preference,
        language=current_user.language,
        total_trips=total_trips,
        total_countries=total_countries,
        total_spent=total_spent,
        achievements_count=achievements_count,
    )

@router.put("/profile", response_model=UserResponse)
async def update_profile(user_data: UserUpdate, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    return await UserService.update(db, current_user.user_id, user_data)

@router.delete("/profile")
async def delete_account(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user = await UserService.get_by_id(db, current_user.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "Account deleted successfully"}
