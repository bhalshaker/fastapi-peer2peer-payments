from fastapi import APIRouter, Depends, HTTPException
from models import UserModel
from controllers import GetCurrentUserController

account_router = APIRouter()

@account_router.get("/api/v1/accounts/me")
async def get_current_user_account(current_user: UserModel = Depends(GetCurrentUserController)):
    pass