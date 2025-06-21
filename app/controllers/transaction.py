from models import TransactionModel
from sqlalchemy.ext.asyncio import AsyncSession
from schema import CreateTransactionSchema
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import or_

async def create_transaction(transaction: CreateTransactionSchema, db: AsyncSession) -> TransactionModel:
    """
    Create a new transaction in the database.

    Args:
        transaction (CreateTransactionSchema): The transaction data to create.
        db (AsyncSession): The database session.

    Returns:
        TransactionModel: The created transaction model.
    """
    new_transaction = TransactionModel(**transaction.model_dump())
    db.add(new_transaction)
    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction

async def get_transactions_by_account_id(account_id: UUID, db: AsyncSession) -> list[TransactionModel]:
    """
    Retrieve all transactions for a specific account.

    Args:
        account_id (UUID): The ID of the account to retrieve transactions for.
        db (AsyncSession): The database session.

    Returns:
        list[TransactionModel]: A list of transaction models associated with the account.
    """
    result = await db.execute(select(TransactionModel).where(
        or_(
            TransactionModel.sender_account_id == account_id,
            TransactionModel.receiver_account_id == account_id
        )
    ))
    return result.scalars().all()