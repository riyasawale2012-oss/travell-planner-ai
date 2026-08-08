from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from enum import Enum

class NotificationType(str, Enum):
    TRIP_REMINDER = "trip_reminder"
    BUDGET_ALERT = "budget_alert"
    BOOKING_CONFIRMED = "booking_confirmed"
    AI_SUGGESTION = "ai_suggestion"
    SYSTEM = "system"

class NotificationBase(BaseModel):
    type: NotificationType
    title: str
    message: Optional[str] = None

class NotificationCreate(NotificationBase):
    user_id: int

class NotificationResponse(NotificationBase):
    model_config = ConfigDict(from_attributes=True)

    notification_id: int
    user_id: int
    is_read: bool
    created_at: datetime
