from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from config import config

#Generate database URL from configuration
db_url=f"postgresql+asyncpg://{config.db_user}:{config.db_password}@{config.db_host}:{config.db_port}/{config.db_name}"
# Create an asynchronous engine and configurre pool size
engine = create_async_engine(db_url, pool_size=config.db_pool_size, max_overflow=config.db_max_overflow)  # Adjust pool size as needed
# Create an asynchronous session factory
SessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with SessionLocal() as session:
        yield session
        
async def recreate_db(Base):
    # Drop and recreate tables to ensure a clean slate
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)