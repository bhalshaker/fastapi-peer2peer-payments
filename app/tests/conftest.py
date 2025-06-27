import sys
import os
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from httpx import ASGITransport, AsyncClient

# Add path to app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from main import app
from database import get_db_session
from models import Base
from schema import CreateUserSchema
from controllers import CreateUserController
from config import config

@pytest_asyncio.fixture(scope="function")
async def db_engine():
    """Create a fresh in-memory database engine for each test."""
    # Use named in-memory database
    test_database_url = f"sqlite+aiosqlite:///:memory:"
    
    # Use StaticPool to maintain a single connection throughout the test
    # This is crucial for in-memory SQLite to work correctly
    engine = create_async_engine(
        test_database_url,
        connect_args={"check_same_thread": False},  # Required for SQLite
        poolclass=StaticPool  # Maintain a single connection
    )
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Clean up
    await engine.dispose()

@pytest_asyncio.fixture(scope="function")
async def db_session(db_engine):
    """Create a fresh database session for each test."""
    # Create session factory for this specific engine
    TestSessionLocal = async_sessionmaker(db_engine, class_=AsyncSession, expire_on_commit=False)
    
    # Create and yield a session
    async with TestSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()

@pytest_asyncio.fixture(scope="function")
async def client(db_session):
    """Get a TestClient with the database session override."""
    # Override the get_db_session dependency
    async def override_get_db_session():
        try:
            yield db_session
        finally:
            pass
    
    # Apply the override
    app.dependency_overrides[get_db_session] = override_get_db_session
    
    # Create test client
    async with AsyncClient(
        transport=ASGITransport(app=app), 
        base_url="http://test"
    ) as test_client:
        yield test_client
    
    # Clean up
    app.dependency_overrides = {}

@pytest_asyncio.fixture(scope="function")
async def create_admin_user(db_session):
    """Create an admin user for testing."""
    # Create an admin user based on the configuration settings
    admin_user = CreateUserSchema(
        username=config.admin_username,
        email=config.admin_email,
        plain_password=config.admin_password,
        first_name=config.admin_first_name,
        last_name=config.admin_last_name
    )
    
    # Use the controller to create the admin user
    admin = await CreateUserController(admin_user, db_session, is_admin=True)
    return admin

@pytest.fixture(scope="session")
def anyio_backend():
    """Return the anyio backend to use."""
    return "asyncio"