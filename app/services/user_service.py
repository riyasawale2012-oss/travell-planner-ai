from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from typing import Optional
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.auth.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        result = await db.execute(select(User).where(User.user_id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def create(db: AsyncSession, user_data: UserCreate) -> User:
        existing = await UserService.get_by_email(db, user_data.email)
        if existing:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
        db_user = User(
            full_name=user_data.full_name, email=user_data.email,
            password=get_password_hash(user_data.password), phone=user_data.phone, role=UserRole.USER,
        )
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update(db: AsyncSession, user_id: int, user_data: UserUpdate) -> User:
        user = await UserService.get_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)
        await db.commit()
        await db.refresh(user)
        return user

    @staticmethod
    async def authenticate(db: AsyncSession, email: str, password: str) -> Optional[User]:
        user = await UserService.get_by_email(db, email)
        if not user or not user.password:
            return None
        if not verify_password(password, user.password):
            return None
        return user

    @staticmethod
    async def change_password(db: AsyncSession, user_id: int, current_password: str, new_password: str) -> bool:
        user = await UserService.get_by_id(db, user_id)
        if not user or not verify_password(current_password, user.password):
            return False
        user.password = get_password_hash(new_password)
        await db.commit()
        return True
