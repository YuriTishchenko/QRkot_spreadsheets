from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Generic, Optional, Type, TypeVar
from pydantic import BaseModel

from app.core.db import Base
from app.models import User


ModelType = TypeVar('ModelType', bound=Base)
CreateSchemaType = TypeVar('CreateSchemaType', bound=BaseModel)
UpdateSchemaType = TypeVar('UpdateSchemaType', bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType]):

    def __init__(
            self,
            model: Type[ModelType]
    ) -> None:
        self.model = model

    async def get(
            self,
            obj_id: int,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получение объекта по id"""
        db_obj = await session.execute(
            select(self.model).where(
                self.model.id == obj_id
            )
        )
        return db_obj.scalars().first()

    async def get_multi(
            self,
            session: AsyncSession,
    ) -> Optional[ModelType]:
        """Получение всех объектов"""
        db_objs = await session.execute(select(self.model))
        return db_objs.scalars().all()

    async def create(
            self,
            obj_in: ModelType,
            session: AsyncSession,
            user: Optional[User] = None
    ) -> ModelType:
        """Создание объекта"""
        obj_in_data = obj_in.dict()
        if user is not None:
            obj_in_data['user_id'] = user.id
        db_obj = self.model(**obj_in_data)
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db_obj: ModelType,
            obj_in: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """обновление объекта"""
        obj_data = jsonable_encoder(db_obj)
        update_data = obj_in.dict(exclude_unset=True)

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj

    async def remove(
            self,
            db_obj: ModelType,
            session: AsyncSession,
    ) -> ModelType:
        """удаление объекта"""
        await session.delete(db_obj)
        await session.commit()
        return db_obj