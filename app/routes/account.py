from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db_session
from models import UserModel
from controllers import GetCurrentUserController,UpdateAccountBalanceController
from schema import TopUpRequestSchema,AccountInfoSchema

account_router = APIRouter()

@account_router.get("/api/v1/accounts/me",response_model=AccountInfoSchema, summary="Get current user's account details",
                     description="Returns the account details of the currently logged-in user, including account ID, balance, and currency.")
async def get_current_user_account(current_user: UserModel = Depends(GetCurrentUserController)):
    if current_user.account is None:
        raise HTTPException(status_code=400, detail="User does not have an account associated with their profile")
    account_details_response = AccountInfoSchema(user_id=current_user.id,
                                               account_id=current_user.account.id,
                                               balance=current_user.account.balance,
                                               currency=current_user.account.currency)
    return account_details_response

@account_router.post("/api/v1/accounts/top-up",response_model=AccountInfoSchema, summary="Top up account",
                     description="Allows the currently logged-in user to top up their account balance.")
async def top_up_account( top_up_data: TopUpRequestSchema,db_session: AsyncSession = Depends(get_db_session),current_user: UserModel = Depends(GetCurrentUserController))->AccountInfoSchema:
    """
    Top up the account of the currently logged-in user.
    
    Args:
        top_up_data (TopUpRequestSchema): The schema containing the top-up amount.
        current_user (UserModel): The currently authenticated user model instance.
        
    Returns:
        dict: A message indicating the success of the top-up operation.
        
    Raises:
        HTTPException: If the top-up amount is invalid or if there is an error processing the top-up.
    """
    if current_user.account is None:
        raise HTTPException(status_code=400, detail="User does not have an account associated with their profile")
    updated_account_details = await UpdateAccountBalanceController(
        account_id=current_user.account.id,
        change_in_balance=top_up_data.amount,
        db=db_session)
    account_details_response=AccountInfoSchema(user_id=current_user.id,
                                               account_id=updated_account_details.id,
                                               balance=updated_account_details.balance,
                                               currency=updated_account_details.currency)
    return account_details_response
