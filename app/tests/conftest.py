import sys
import os
# Ensure the project root is in sys.path for module resolution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import sessionmaker
from main import app
from database import get_db_session
from datetime import datetime
from models import Base
from config import config

@pytest.fixture(scope="session")
def anyio_backend():
    return 'asyncio'

@pytest.fixture(autouse=True, scope="function")
def apply_db_session_override():
    if config.use_testcontainers:
        from testcontainers.postgres import PostgresContainer
        with PostgresContainer("postgres:17") as postgres:
            sync_database_url = postgres.get_connection_url()
            async_database_url = sync_database_url.replace("postgresql://", "postgresql+asyncpg://")
            test_engine = create_async_engine(async_database_url, pool_size=config.db_pool_size, max_overflow=config.db_max_overflow)
            TestSessionLocal = async_sessionmaker(
                bind=test_engine,
                expire_on_commit=False,)
            async def _override_get_db_session():
                async with TestSessionLocal() as session:
                    try:
                        yield session
                    finally:
                        await session.close()
            app.dependency_overrides[get_db_session] = _override_get_db_session
            yield
            app.dependency_overrides = {}
    else:
        SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
        test_engine = create_async_engine(SQLALCHEMY_DATABASE_URL, echo=False)
        TestSessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=test_engine)    
        async def _override_get_db_session():
            async with TestSessionLocal() as session:
                try:
                    yield session
                finally:
                    await session.close()
        app.dependency_overrides[get_db_session] = _override_get_db_session
        yield
        app.dependency_overrides = {}

@pytest.fixture(autouse=True,scope="function")
async def create_test_db():
    """
    Create the database schema for testing before any tests run.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    yield