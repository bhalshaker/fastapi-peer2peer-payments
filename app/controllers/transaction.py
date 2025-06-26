from fastapi import HTTPException,status
from models import TransactionModel,TransactionStatus,AccountModel
from sqlalchemy.ext.asyncio import AsyncSession
from schema import CreateTransactionRequestSchema,TransactionInfoSchema,TransactionsOfUserSchema
from uuid import UUID
from sqlalchemy.future import select
from sqlalchemy import or_
from .user import get_user_by_id
from .account import get_account_by_id
from utilities import ConvertCurrencyUtility
from .account import update_account_balance


async def create_transaction(transaction: TransactionModel, db: AsyncSession) -> TransactionModel:
    """
    Create a new transaction in the database.

    Args:
        transaction (CreateTransactionSchema): The transaction data to create.
        db (AsyncSession): The database session.

    Returns:
        TransactionModel: The created transaction model.
    """
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction)
    return transaction

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

async def get_user_transactions(user_id: UUID, db: AsyncSession) -> TransactionsOfUserSchema:
    """
    Retrieve all transactions for a specific user.

    Args:
        user_id (UUID): The ID of the user to retrieve transactions for.
        db (AsyncSession): The database session.

    Returns:
        TransactionsOfUserSchema: A schema containing the user's transaction history.
    """
    user = await get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found.")
    
    transactions = await get_transactions_by_account_id(user.account.id, db)
    
    return TransactionsOfUserSchema(
        user_id=user.id,
        transactions=[
            TransactionInfoSchema(
                sender_account_id=transaction.sender_account_id,
                receiver_account_id=transaction.receiver_account_id,
                amount=transaction.amount,
                from_currency=transaction.from_currency,
                to_currency=transaction.to_currency,
                exchange_rate=transaction.exchange_rate,
                status=transaction.status
            ) for transaction in transactions
        ]
    )

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
    # Get receiver account
    receiver_account = await get_account_by_id(transaction.receiver_account_id, db)
    if not receiver_account:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Receiver account not found.")
    
    # Calculate transaction amount based on exchange rate
    receiver_amount = transaction.amount
    exchange_rate= 1.0
    if sender_account.currency != receiver_account.currency:
        exchange_convertion_data = ConvertCurrencyUtility(sender_account.currency, receiver_account.currency, transaction.amount)
        receiver_amount = exchange_convertion_data['converted_amount']
        exchange_rate = exchange_convertion_data['exchange_rate']

    # Deduct amount from sender's account balanace
    await update_account_balance(
        account_id=sender_account.id,
        amount=-transaction.amount,  # Deduct the amount from sender's balance
        db=db
    )
    # Topup amount to receiver balance
    await update_account_balance(
        account_id=receiver_account.id,
        amount=receiver_amount,  # Add the converted amount to receiver's balance
        db=db
    )
    # Record the transaction
    transaction_model = TransactionModel(
        sender_account_id=sender_account.id,
        receiver_account_id=receiver_account.id,
        amount=transaction.amount,
        from_currency=sender_account.currency,
        to_currency=receiver_account.currency,
        exchange_rate=exchange_rate,
        status=TransactionStatus.COMPLETED  # Assuming the transaction is successful
    )
    new_transaction = await create_transaction(transaction_model, db)
    return TransactionInfoSchema(
        sender_account_id=new_transaction.sender_account_id,
        receiver_account_id=new_transaction.receiver_account_id,
        amount=new_transaction.amount,
        from_currency=new_transaction.from_currency,
        to_currency=new_transaction.to_currency,
        exchange_rate=new_transaction.exchange_rate,
        status=new_transaction.status
    )