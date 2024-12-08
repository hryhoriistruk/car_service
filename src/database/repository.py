from datetime import datetime
from typing import Generic, TypeVar

from fastapi_users_db_sqlalchemy import UUID_ID
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

Model = TypeVar("Model", bound=DeclarativeBase)


class DatabaseRepository(Generic[Model]):
    """
    Database repository for CRUD operations.

    Args:
        Type[Model]: SQLAlchemy model class.
    """

    def __init__(self, model: type[Model], session: AsyncSession) -> None:
        self.model = model
        self.session = session

    async def get(self, pk: int | UUID_ID) -> Model | None:
        return await self.session.get(self.model, pk)

    async def create(self, data: BaseModel) -> Model:
        instance = self.model(**data.model_dump())
        self.session.add(instance)
        await self.session.commit()
        await self.session.refresh(instance)
        return instance

    async def update(self, data: BaseModel, pk: int | UUID_ID) -> Model | str:
        item = await self.get(pk)
        if not item:
            return f'{self.model.__name__} with id={pk} not found.'
        try:
            for key, value in data.model_dump().items():
                setattr(item, key, value)
            item.updated = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(item)
            return item
        except IntegrityError as e:
            return str(e)

    async def delete(self, pk: int | UUID_ID) -> bool:
        item = await self.get(pk)
        if not item:
            return False
        await self.session.delete(item)
        await self.session.commit()
        return True
