from fastapi import HTTPException
from .user import get_user_by_username
from schema import LoginUserSchema, TokenResponseSchema
from sqlalchemy.ext.asyncio import AsyncSession
from utilities import verify_password,generate_token

async def login(use_login: LoginUserSchema,db_session: AsyncSession):
    retrieved_user = await get_user_by_username(use_login.username,db_session)
    if retrieved_user:
        if await verify_password(use_login.password):
            return await generate_token(retrieved_user.id, retrieved_user.is_admin)
        else:
            raise HTTPException(status_code=401, detail="Incorrect combination of username and password")
    else:
        raise HTTPException(status_code=401, detail="Incorrect combination of username and password")