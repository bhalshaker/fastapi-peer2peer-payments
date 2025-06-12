from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from models import UserModel
from schema import CreateUserSchema

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