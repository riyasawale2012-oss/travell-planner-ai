from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, func, and_
from typing import List, Optional
from app.models.notification import Notification, NotificationType

class NotificationService:
    @staticmethod
    async def create(db: AsyncSession, user_id: int, type: NotificationType, title: str, message: Optional[str] = None) -> Notification:
        notification = Notification(user_id=user_id, type=type, title=title, message=message)
        db.add(notification)
        await db.commit()
        await db.refresh(notification)
        return notification

    @staticmethod
    async def get_user_notifications(db: AsyncSession, user_id: int, unread_only: bool = False, page: int = 1, per_page: int = 20):
        query = select(Notification).where(Notification.user_id == user_id)
        if unread_only:
            query = query.where(Notification.is_read == False)
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar()
        query = query.order_by(Notification.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await db.execute(query)
        return result.scalars().all(), total

    @staticmethod
    async def mark_as_read(db: AsyncSession, notification_id: int, user_id: int) -> bool:
        result = await db.execute(update(Notification).where(and_(Notification.notification_id == notification_id, Notification.user_id == user_id)).values(is_read=True))
        await db.commit()
        return result.rowcount > 0

    @staticmethod
    async def mark_all_as_read(db: AsyncSession, user_id: int) -> bool:
        await db.execute(update(Notification).where(and_(Notification.user_id == user_id, Notification.is_read == False)).values(is_read=True))
        await db.commit()
        return True

    @staticmethod
    async def get_unread_count(db: AsyncSession, user_id: int) -> int:
        result = await db.execute(select(func.count()).where(and_(Notification.user_id == user_id, Notification.is_read == False)))
        return result.scalar() or 0
