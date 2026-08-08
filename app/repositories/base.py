from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, inspect
from typing import Generic, TypeVar, Type, Optional, List

ModelType = TypeVar("ModelType")

class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], db: AsyncSession):
        self.model = model
        self.db = db

    def _primary_key_attr(self):
        mapper = inspect(self.model)
        return mapper.primary_key[0]

    async def get_by_id(self, id: int) -> Optional[ModelType]:
        pk = self._primary_key_attr()
        result = await self.db.execute(select(self.model).where(pk == id))
        return result.scalar_one_or_none()

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        result = await self.db.execute(select(self.model).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, obj_in: dict) -> ModelType:
        db_obj = self.model(**obj_in)
        self.db.add(db_obj)
        await self.db.commit()
        await self.db.refresh(db_obj)
        return db_obj

    async def update(self, id: int, obj_in: dict) -> Optional[ModelType]:
        pk = self._primary_key_attr()
        await self.db.execute(update(self.model).where(pk == id).values(**obj_in))
        await self.db.commit()
        return await self.get_by_id(id)

    async def delete(self, id: int) -> bool:
        pk = self._primary_key_attr()
        result = await self.db.execute(delete(self.model).where(pk == id))
        await self.db.commit()
        return result.rowcount > 0
