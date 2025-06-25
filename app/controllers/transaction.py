from models import TransactionModel,TransactionStatus,AccountModel
from sqlalchemy.ext.asyncio import AsyncSession
from schema import CreateTransactionRequestSchema,TransactionInfoSchema
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import or_
from .user import get_user_by_id

async def create_transaction(transaction: CreateTransactionRequestSchema,sender_account_id:UUID, db: AsyncSession) -> TransactionModel:
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

async def carry_out_transaction(transaction: CreateTransactionRequestSchema,sender_account:AccountModel, db: AsyncSession) -> TransactionInfoSchema:
    """
    Carry out a transaction by creating it in the database and returning its information.

    Args:
        transaction (CreateTransactionRequestSchema): The transaction data to carry out.
        sender_account_id (UUID): The ID of the sender's account.
        db (AsyncSession): The database session.

    Returns:
        TransactionInfoSchema: The information of the carried out transaction.
    """

    new_transaction = await create_transaction(transaction, sender_account.id, db)
    return TransactionInfoSchema(
        sender_account_id=new_transaction.sender_account_id,
        receiver_account_id=new_transaction.receiver_account_id,
        amount=new_transaction.amount,
        from_currency=new_transaction.from_currency,
        to_currency=new_transaction.to_currency,
        exchange_rate=new_transaction.exchange_rate,
        status=TransactionStatus(new_transaction.status).name
    )