from fastapi import APIRouter, Depends, HTTPException
from schema import LoginUserSchema,TokenResponseSchema
from database import get_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from controllers import LoginController
auth_router = APIRouter()

@auth_router.post("/api/v1/auth/login",summary="Login User", response_model=TokenResponseSchema)
async def login(use_login: LoginUserSchema,db_session: AsyncSession = Depends(get_db_session)):
    return await LoginController(use_login, db_session)

@auth_router.post("/api/v1/auth/signup")
async def signup():
    pass