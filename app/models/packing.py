from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.database.base import Base

class PackingList(Base):
    __tablename__ = "packing_lists"
    packing_id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id", ondelete="CASCADE"), nullable=False)
    item_name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=True)
    is_packed = Column(Boolean, default=False)
    is_essential = Column(Boolean, default=False)
    quantity = Column(Integer, default=1)
    trip = relationship("Trip", back_populates="packing_lists")
