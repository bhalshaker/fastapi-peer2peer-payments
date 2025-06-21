from sqlalchemy.ext.asyncio import AsyncSession
from models import AccountModel
from schema import CreateAccountSchema

async def create_account(user:CreateAccountSchema, db: AsyncSession) -> AccountModel:
    pass