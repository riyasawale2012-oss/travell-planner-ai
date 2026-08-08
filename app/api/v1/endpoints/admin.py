from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional
from app.database.session import get_db
from app.auth.dependencies import get_current_admin
from app.models.user import User
from app.models.trip import Trip
from app.models.expense import Expense
from app.models.review import Review

router = APIRouter()

@router.get("/dashboard")
async def admin_dashboard(admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    total_users = await db.execute(select(func.count()).select_from(User))
    total_trips = await db.execute(select(func.count()).select_from(Trip))
    total_expenses = await db.execute(select(func.sum(Expense.amount)))
    total_reviews = await db.execute(select(func.count()).select_from(Review))
    recent_users = await db.execute(select(User).order_by(User.created_at.desc()).limit(5))
    return {
        "stats": {
            "total_users": total_users.scalar(),
            "total_trips": total_trips.scalar(),
            "total_expenses": float(total_expenses.scalar() or 0),
            "total_reviews": total_reviews.scalar(),
        },
        "recent_users": recent_users.scalars().all(),
    }

@router.get("/users")
async def list_users(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    admin = Depends(get_current_admin),
    db: AsyncSession = Depends(get_db)
):
    query = select(User).order_by(User.created_at.desc())
    count_result = await db.execute(select(func.count()).select_from(query.subquery()))
    total = count_result.scalar()
    query = query.offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(query)
    return {"users": result.scalars().all(), "total": total, "page": page, "per_page": per_page}

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, admin = Depends(get_current_admin), db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    await db.delete(user)
    await db.commit()
    return {"message": "User deleted successfully"}
