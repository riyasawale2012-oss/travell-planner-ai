from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.auth.dependencies import get_current_user
from app.services.notification_service import NotificationService
from app.models.user import User

router = APIRouter()

@router.get("")
async def get_notifications(
    unread_only: bool = False,
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    notifications, total = await NotificationService.get_user_notifications(db, current_user.user_id, unread_only, page, per_page)
    return {"notifications": notifications, "total": total, "page": page, "per_page": per_page}

@router.get("/unread-count")
async def get_unread_count(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    count = await NotificationService.get_unread_count(db, current_user.user_id)
    return {"unread_count": count}

@router.post("/{notification_id}/read")
async def mark_read(notification_id: int, current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    success = await NotificationService.mark_as_read(db, notification_id, current_user.user_id)
    return {"success": success}

@router.post("/read-all")
async def mark_all_read(current_user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    await NotificationService.mark_all_as_read(db, current_user.user_id)
    return {"message": "All notifications marked as read"}
