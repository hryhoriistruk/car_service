from typing import Callable

from database.repository import DatabaseRepository
from database.session import get_async_session
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase


def get_repository(
        model: type[DeclarativeBase],
        repo_type: type[DatabaseRepository],
) -> Callable[[AsyncSession], DatabaseRepository]:
    def func(session: AsyncSession = Depends(get_async_session)):
        return repo_type(model, session)

    return func
