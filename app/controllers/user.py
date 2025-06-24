from fastapi import HTTPException,status
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from schema import CreateUserSchema, CreateAccountSchema,UserInfoSchema
from uuid import UUID
from .account import create_account

async def create_user(user:CreateUserSchema, db: AsyncSession, is_admin:bool=False) -> UserModel:
    """
    Create a new user in the database.
    
    Args:
        user (CreateUserSchema): The user data to create.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel: The created user model.
    """
    new_user = UserModel(**user.model_dump(exclude={"plain_password","account_currency"}),is_admin=is_admin)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(user_id: UUID, db: AsyncSession) -> UserModel | None:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id (UUID): The ID of the user to retrieve.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel | None: The user model if found, otherwise None.
    """
    result = await db.execute(select(UserModel).options(selectinload(UserModel.account)).where(UserModel.id == user_id))
    return result.scalars().first()

async def get_user_by_username(username: str, db: AsyncSession) -> UserModel | None:
    """
    Retrieve a user by their username.
    
    Args:
        username (str): The username of the user to retrieve.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel | None: The user model if found, otherwise None.
    """
    result = await db.execute(select(UserModel).where(UserModel.username == username))
    return result.scalars().first()
# Get user by username or email
async def get_user_by_username_email(username: str,email:str, db: AsyncSession) -> UserModel | None:
    """ Retrieve a user by their username or email."""
    result = await db.execute(
        select(UserModel).where(
            (UserModel.username == username) | (UserModel.email == email)
        )
    )
    return result.scalars().first()

async def signup_user(user: CreateUserSchema, db: AsyncSession) -> UserInfoSchema:
    """
    Sign up a new user.
    
    Args:
        user (CreateUserSchema): The user data to sign up.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel: The created user model.
    """
    #Check if username or email already exists
    existing_user = await get_user_by_username_email(user.username,user.email, db)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already exists.")
    new_user=await create_user(user, db, False)
    create_account_schema= CreateAccountSchema(
        user_id=new_user.id,
        currency=user.account_currency
    )
    new_account= await create_account(create_account_schema,db)
    user_info = UserInfoSchema(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        first_name=new_user.first_name,
        middle_name=new_user.middle_name,
        last_name=new_user.last_name,
        is_admin=new_user.is_admin,
        account_id=new_account.id
    )
    return user_info