from sqlalchemy import Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class TravelPreference(Base):
    __tablename__ = "travel_preferences"
    preference_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False, unique=True)
    adventure = Column(Boolean, default=False)
    shopping = Column(Boolean, default=False)
    food = Column(Boolean, default=False)
    culture = Column(Boolean, default=False)
    nature = Column(Boolean, default=False)
    nightlife = Column(Boolean, default=False)
    relaxation = Column(Boolean, default=False)
    photography = Column(Boolean, default=False)
    user = relationship("User", back_populates="preferences")
