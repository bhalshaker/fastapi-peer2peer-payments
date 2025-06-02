from enum import Enum
from .base import BaseModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum,VARCHAR,BOOLEAN
from sqlalchemy.orm import relationship


class UserStatus(Enum):
    """
    Enumeration of possible user account statuses in the system.
    Values:
        ACTIVE: User account is active and can perform all operations.
        SUSPENDED: User account is temporarily suspended and restricted from certain operations.
        CLOSED: User account is permanently closed and cannot perform operations.
    """

    ACTIVE = 'active'
    SUSPENDED = 'suspended'
    CLOSED = 'closed'

class UserModel(BaseModel):
    """
    User model representing users in the system.
    This model stores personal information about users and their system access rights.
    Each user can have an associated account linked through a one-to-many relationship.
    Attributes:
        user_name (str): Username for the user. Must be unique, maximum 50 characters.
        email (str): Email address of the user. Must be unique, maximum 100 characters.
        password (str): Hashed password for the user. Maximum 255 characters.
        first_name (str): User's first name. Maximum 50 characters.
        middle_name (str): User's middle name. Maximum 50 characters, optional.
        last_name (str): User's last name. Maximum 50 characters.
        is_admin (bool): Flag indicating if the user has admin privileges. Defaults to False.
        user_status (UserStatus): Current status of the user. Defaults to UserStatus.ACTIVE.
        account (AccountModel): Relationship to the user's account.
    Table: users
    """

    __tablename__ = 'users'
    
    user_name = Column(VARCHAR(50), nullable=False, unique=True)
    email = Column(VARCHAR(100), nullable=False, unique=True)
    password = Column(VARCHAR(255), nullable=False)
    first_name = Column(VARCHAR(50), nullable=False)
    middle_name = Column(VARCHAR(50), nullable=True)
    last_name = Column(VARCHAR(50), nullable=False)
    is_admin = Column(BOOLEAN, nullable=False, default=False)
    user_status = Column(SQLAlchemyEnum(UserStatus), nullable=False, default=UserStatus.ACTIVE)
    account= relationship('AccountModel', back_populates='user')