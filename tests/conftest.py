import sys

import pytest_asyncio



sys.path.append("..")
from src.app.ref_system.models import referral_code
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from src.config import DB_USER_TEST, DB_PASS_TEST, DB_HOST_TEST, DB_PORT_TEST, DB_NAME_TEST
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy import NullPool, select
from src.database import get_async_session
from src.database import metadata as base_metadata
from src.main import create_app

TEST_DATABASE_URL = f'postgresql+asyncpg://{DB_USER_TEST}:{DB_PASS_TEST}@{DB_HOST_TEST}:{DB_PORT_TEST}/{DB_NAME_TEST}'

engine_test = create_async_engine(TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker_test = async_sessionmaker(bind=engine_test, class_=AsyncSession, expire_on_commit=False)
base_metadata.bind = engine_test


@pytest_asyncio.fixture(scope="session", autouse=True)
async def create_migration():
	async with engine_test.begin() as connection:
		await connection.run_sync(base_metadata.create_all)
	yield
	async with engine_test.begin() as connection:
		await connection.run_sync(base_metadata.drop_all)


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
	async with async_session_maker_test() as async_session:
		yield async_session


@pytest_asyncio.fixture(scope="session")
async def ac() -> AsyncGenerator[AsyncClient, None]:
	app = create_app()
	app.dependency_overrides[get_async_session] = override_get_async_session
	async with AsyncClient(app=app, base_url='http://localhost:8000') as ac:
		yield ac


@pytest_asyncio.fixture(scope='function')
async def get_ref_code():
	async with async_session_maker_test() as session:
		ref_code = await session.scalar(select(referral_code.c.code))
		return ref_code
