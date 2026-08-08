from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from fastapi import HTTPException
from typing import List, Optional
from decimal import Decimal
from app.models.expense import Expense, ExpenseCategory
from app.models.trip import Trip
from app.schemas.expense import ExpenseCreate, ExpenseUpdate, ExpenseSummary

class ExpenseService:
    @staticmethod
    async def create(db: AsyncSession, expense_data: ExpenseCreate) -> Expense:
        trip = await db.get(Trip, expense_data.trip_id)
        if not trip:
            raise HTTPException(status_code=404, detail="Trip not found")
        db_expense = Expense(**expense_data.model_dump())
        db.add(db_expense)
        await db.commit()
        await db.refresh(db_expense)
        return db_expense

    @staticmethod
    async def get_by_id(db: AsyncSession, expense_id: int, user_id: int) -> Optional[Expense]:
        result = await db.execute(
            select(Expense).join(Trip).where(and_(Expense.expense_id == expense_id, Trip.user_id == user_id))
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_trip_expenses(db: AsyncSession, trip_id: int, user_id: int, category: Optional[ExpenseCategory] = None, page: int = 1, per_page: int = 50):
        query = select(Expense).join(Trip).where(and_(Expense.trip_id == trip_id, Trip.user_id == user_id))
        if category:
            query = query.where(Expense.category == category)
        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar()
        query = query.order_by(Expense.expense_date.desc()).offset((page - 1) * per_page).limit(per_page)
        result = await db.execute(query)
        return result.scalars().all(), total

    @staticmethod
    async def update(db: AsyncSession, expense_id: int, user_id: int, data: ExpenseUpdate) -> Expense:
        expense = await ExpenseService.get_by_id(db, expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        update_data = data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(expense, field, value)
        await db.commit()
        await db.refresh(expense)
        return expense

    @staticmethod
    async def delete(db: AsyncSession, expense_id: int, user_id: int) -> bool:
        expense = await ExpenseService.get_by_id(db, expense_id, user_id)
        if not expense:
            raise HTTPException(status_code=404, detail="Expense not found")
        await db.delete(expense)
        await db.commit()
        return True

    @staticmethod
    async def get_expense_summary(db: AsyncSession, trip_id: int, user_id: int) -> List[ExpenseSummary]:
        result = await db.execute(
            select(Expense.category, func.sum(Expense.amount).label("total"), func.count().label("count"))
            .join(Trip).where(and_(Expense.trip_id == trip_id, Trip.user_id == user_id))
            .group_by(Expense.category)
        )
        total_result = await db.execute(
            select(func.sum(Expense.amount)).join(Trip).where(and_(Expense.trip_id == trip_id, Trip.user_id == user_id))
        )
        total_spent = total_result.scalar() or Decimal("0")
        summaries = []
        for row in result.all():
            percentage = (float(row.total) / float(total_spent) * 100) if total_spent > 0 else 0
            summaries.append(ExpenseSummary(category=row.category, total=row.total, percentage=round(percentage, 2), count=row.count))
        return summaries

    @staticmethod
    async def get_total_spent(db: AsyncSession, trip_id: int, user_id: int) -> Decimal:
        result = await db.execute(
            select(func.sum(Expense.amount)).join(Trip).where(and_(Expense.trip_id == trip_id, Trip.user_id == user_id))
        )
        return result.scalar() or Decimal("0")
