from fastapi import APIRouter, Depends, HTTPException,status
from schema import CreateTransactionRequestSchema,TransactionInfoSchema,TransactionsOfUserSchema
from database import get_db_session
from controllers import GetCurrentUserController,CarryOutTransactionController,GetUserTransactionsController
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel,TransactionModel
from uuid import UUID

transaction_router = APIRouter()

@transaction_router.post("/api/v1/transactions/send"
                         , response_model=TransactionInfoSchema,
                         summary="Transfer money between accounts",
                         description="This endpoint allows users to transfer money from one account to another. ")
async def transfer_money(tranaction_request:CreateTransactionRequestSchema,current_user:UserModel=Depends(GetCurrentUserController)
                         ,db_session:AsyncSession=Depends(get_db_session))-> TransactionInfoSchema:
    if current_user.account.balance < tranaction_request.amount:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient balance for the transaction.")
    return await CarryOutTransactionController(tranaction_request, current_user.account, db_session)

@transaction_router.get("/api/v1/transactions/history",
                        response_model=TransactionsOfUserSchema,
                        summary="Get transaction history",
                        description="This endpoint retrieves the transaction history for the current user.")
async def get_transaction_history(current_user:UserModel=Depends(GetCurrentUserController)
                         ,db_session:AsyncSession=Depends(get_db_session)) -> TransactionsOfUserSchema:
    return await GetUserTransactionsController(current_user.id, db_session)

@transaction_router.get("/api/v1/transactions/{user_id}",
                        response_model=TransactionsOfUserSchema,
                        summary="Get transaction history for a specific user",
                        description="This endpoint retrieves the transaction history for a specific user. "
                                    "Only accessible by admins.")
async def get_user_transaction_history(user_id: str,current_user:UserModel=Depends(GetCurrentUserController)
                         ,db_session:AsyncSession=Depends(get_db_session)) -> TransactionsOfUserSchema:
    if not current_user.is_admin:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Access denied. Admins only.")
    return await GetUserTransactionsController(UUID(user_id), db_session)