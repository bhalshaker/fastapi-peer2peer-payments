from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker
from config import config

#Generate database URL from configuration
db_url=f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
# Create an asynchronous engine and configurre pool size
engine = create_async_engine(db_url, pool_size=config.db_pool_size, max_overflow=config.db_max_overflow)  # Adjust pool size as needed
# Create an asynchronous session factory using async_sessionmaker
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Yields a database session as a dependency that can be used in FastAPI routes.
    
    Usage in FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db_session)):
            ...
    """
    async with SessionLocal() as session:
        yield session