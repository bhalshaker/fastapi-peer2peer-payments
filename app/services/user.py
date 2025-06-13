from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from schema import CreateUserSchema
from uuid import UUID

async def create_user(user:CreateUserSchema, db: AsyncSession, is_admin:bool=False) -> UserModel:
    """
    Create a new user in the database.
    
    Args:
        user (CreateUserSchema): The user data to create.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel: The created user model.
    """
    new_user = UserModel(**user.model_dump(exclude={"plain_password"},is_admin=is_admin))
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

async def get_user_by_id(user_id: int, db: AsyncSession) -> UserModel | None:
    """
    Retrieve a user by their ID.
    
    Args:
        user_id (int): The ID of the user to retrieve.
        db (AsyncSession): The database session.
    
    Returns:
        UserModel | None: The user model if found, otherwise None.
    """
    result = await db.execute(select(UserModel).options(UserModel.account).where(UserModel.id == UUID(user_id)))
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