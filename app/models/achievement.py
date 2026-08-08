from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.base import Base

class Achievement(Base):
    __tablename__ = "achievements"
    achievement_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    badge_url = Column(String(500), nullable=True)
    criteria = Column(String(100), nullable=True)
    earned_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="achievements")
