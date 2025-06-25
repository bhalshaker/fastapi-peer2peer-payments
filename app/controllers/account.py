from sqlalchemy.ext.asyncio import AsyncSession
from models import AccountModel
from schema import CreateAccountSchema
from uuid import UUID
from sqlalchemy.future import select

async def create_account(account:CreateAccountSchema, db: AsyncSession) -> AccountModel:
    await db.flush()
    new_account = AccountModel(**account.model_dump())
    db.add(new_account)
    await db.commit()
    await db.refresh(new_account)
    return new_account

async def get_account_by_id(account_id: UUID, db: AsyncSession) -> AccountModel | None:
    """
    Retrieve an account by its ID.
    
    Args:
        account_id (UUID): The ID of the account to retrieve.
        db (AsyncSession): The database session.
    
    Returns:
        AccountModel | None: The account model if found, otherwise None.
    """
    result = await db.execute(select(AccountModel).where(AccountModel.id == account_id))
    return result.scalars().first()

async def update_account_balance(account_id: UUID, change_in_balance: float, db: AsyncSession) -> AccountModel | None:
    """
    Update the balance of an account.
    
    Args:
        account_id (UUID): The ID of the account to update.
        change_in_balance (float): The balance to be changed.
        db (AsyncSession): The database session.
    
    Returns:
        AccountModel | None: The updated account model if found, otherwise None.
    """
    account = await get_account_by_id(account_id, db)
    if account:
        account.balance = account.balance+change_in_balance
        await db.commit()
        await db.refresh(account)
    return account