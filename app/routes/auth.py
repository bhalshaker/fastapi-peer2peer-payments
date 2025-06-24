from fastapi import APIRouter, Depends, HTTPException,status
from schema import LoginUserSchema,TokenResponseSchema,CreateUserSchema,UserInfoSchema
from database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from controllers import LoginController,SignupUserController
from .miscellaneous import get_currencies_list
auth_router = APIRouter()

@auth_router.post("/api/v1/auth/login",summary="Login User", response_model=TokenResponseSchema)
async def login(use_login: LoginUserSchema,db_session: AsyncSession = Depends(get_db_session)):
    return await LoginController(use_login, db_session)

@auth_router.post("/api/v1/auth/signup",response_model=UserInfoSchema,summary="Signup User",
    description="Create a new user account",
    responses={400: {"description": "Bad Request - Username or email already exists",
                     "content": {"application/json": 
                                 {"example": {"detail": "Username or email already exists."}}}}}
    )
async def signup(new_user: CreateUserSchema,db_session: AsyncSession = Depends(get_db_session)):
    # Ensure currencies list is loaded before signup
    currencies_list=await get_currencies_list()
    new_user.account_currency = new_user.account_currency.lower()
    if new_user.account_currency not in currencies_list:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=
                            {"detail": [{"loc": [
                "body",
                "account_currency"
            ],
            "msg": "Invalid currency code.",
            "type": "invalid_currency_code"
        }
    ]})
    return await SignupUserController(new_user, db_session)