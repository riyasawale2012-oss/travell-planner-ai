from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from sqlalchemy.orm import selectinload
from fastapi import HTTPException
from typing import List, Optional
from datetime import date
from decimal import Decimal
from app.models.trip import Trip, TripStatus
from app.models.budget import BudgetAllocation
from app.schemas.trip import TripCreate, TripUpdate

class TripService:
    @staticmethod
    async def create(db: AsyncSession, user_id: int, trip_data: TripCreate) -> Trip:
        duration = (trip_data.end_date - trip_data.start_date).days
        db_trip = Trip(
            user_id=user_id, source=trip_data.source, destination=trip_data.destination,
            destination_country=trip_data.destination_country, is_international=trip_data.is_international,
            start_date=trip_data.start_date, end_date=trip_data.end_date, duration_days=duration,
            total_budget=trip_data.total_budget, currency=trip_data.currency,
            num_travellers=trip_data.num_travellers, travel_style=trip_data.travel_style,
            hotel_category=trip_data.hotel_category, transport_mode=trip_data.transport_mode,
            notes=trip_data.notes,
        )
        db.add(db_trip)
        await db.commit()
        await db.refresh(db_trip)
        await TripService._create_default_budget(db, db_trip)
        return db_trip

    @staticmethod
    async def _create_default_budget(db: AsyncSession, trip: Trip):
        total = float(trip.total_budget)
        if trip.is_international:
            allocation = BudgetAllocation(
                trip_id=trip.trip_id,
                transport_budget=Decimal(str(total * 0.35)), accommodation_budget=Decimal(str(total * 0.25)),
                food_budget=Decimal(str(total * 0.15)), activities_budget=Decimal(str(total * 0.10)),
                shopping_budget=Decimal(str(total * 0.05)), insurance_budget=Decimal(str(total * 0.03)),
                visa_budget=Decimal(str(total * 0.02)), emergency_budget=Decimal(str(total * 0.03)),
                miscellaneous_budget=Decimal(str(total * 0.02)),
            )
        else:
            allocation = BudgetAllocation(
                trip_id=trip.trip_id,
                transport_budget=Decimal(str(total * 0.25)), accommodation_budget=Decimal(str(total * 0.30)),
                food_budget=Decimal(str(total * 0.20)), activities_budget=Decimal(str(total * 0.15)),
                shopping_budget=Decimal(str(total * 0.05)), emergency_budget=Decimal(str(total * 0.03)),
                miscellaneous_budget=Decimal(str(total * 0.02)),
            )
        db.add(allocation)
        await db.commit()

    @staticmethod
    async def get_by_id(db: AsyncSession, trip_id: int, user_id: int) -> Optional[Trip]:
        result = await db.execute(
            select(Trip).options(selectinload(Trip.budget))
            .where(and_(Trip.trip_id == trip_id, Trip.user_id == user_id))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_trips(db: AsyncSession, user_id: int, status: Optional[TripStatus] = None, page: int = 1, per_page: int = 20):
        query = select(Trip).where(Trip.user_id == user_id)
        if status:
            query = query.where(Trip.status == status)
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar()
        query = query.order_by(Trip.created_at.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await db.execute(query)
        return result.scalars().all(), total

    @staticmethod
    async def update(db: AsyncSession, trip_id: int, user_id: int, trip_data: TripUpdate) -> Trip:
        trip = await TripService.get_by_id(db, trip_id, user_id)
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        update_data = trip_data.model_dump(exclude_unset=True)
        if "end_date" in update_data and trip.start_date:
            update_data["duration_days"] = (update_data["end_date"] - trip.start_date).days
        for field, value in update_data.items():
            setattr(trip, field, value)
        await db.commit()
        await db.refresh(trip)
        return trip

    @staticmethod
    async def delete(db: AsyncSession, trip_id: int, user_id: int) -> bool:
        trip = await TripService.get_by_id(db, trip_id, user_id)
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        await db.delete(trip)
        await db.commit()
        return True

    @staticmethod
    async def get_trip_stats(db: AsyncSession, user_id: int) -> dict:
        total_trips = await db.execute(select(func.count()).where(Trip.user_id == user_id))
        upcoming = await db.execute(select(func.count()).where(and_(Trip.user_id == user_id, Trip.start_date >= date.today())))
        total_budget = await db.execute(select(func.sum(Trip.total_budget)).where(Trip.user_id == user_id))
        return {
            "total_trips": total_trips.scalar() or 0,
            "upcoming_trips": upcoming.scalar() or 0,
            "total_budget_planned": float(total_budget.scalar() or 0),
        }
