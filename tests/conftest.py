import asyncio

import pytest
import pytest_asyncio
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker, create_async_engine

from src.config import db_settings
from src.database.models import Base
from src.database.session import get_async_session
from src.main import app


@pytest.fixture(scope='session', autouse=True)
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session')
async def db_engine():
    db_url = f'{db_settings.url}_test'
    engine = create_async_engine(db_url)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return engine


@pytest_asyncio.fixture(scope='session', autouse=True)
async def get_test_session(db_engine: AsyncEngine):
    async_session = async_sessionmaker(db_engine, expire_on_commit=False, autoflush=False)
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture(scope='session')
async def client(get_test_session):
    async def override_get_db():
        try:
            yield get_test_session
        finally:
            await get_test_session.close()

    app.dependency_overrides[get_async_session] = override_get_db
    async with AsyncClient(app=app, base_url="http://127.0.0.1:8000") as async_client:
        yield async_client
