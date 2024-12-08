from typing import AsyncGenerator

from database.models import User
from fastapi import Depends
from fastapi_users.models import UP
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.config import db_settings

DATABASE_URL = db_settings.url

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, expire_on_commit=False, autoflush=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        except SQLAlchemyError:
            await session.rollback()
            raise


class CustomUserDatabase(SQLAlchemyUserDatabase):
    """
    Overloaded database adapter for SQLAlchemy.
    """

    async def get_by_email(self, username: str) -> UP | None:
        """ Overloaded method to get user by username instead of email. """
        statement = select(self.user_table).where(self.user_table.username == username)
        return await self._get_user(statement)


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield CustomUserDatabase(session, User)
