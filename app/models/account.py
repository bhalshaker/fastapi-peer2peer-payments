from enum import Enum
from .base import BaseModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum,UUID,ForeignKey,Numeric,VARCHAR
from sqlalchemy.orm import relationship

class AccountStatus(Enum):
    """
    Enumeration representing the possible statuses of a user account.
    Attributes:
        ACTIVE (str): Account is operational and can perform all transactions.
        CLOSED (str): Account has been permanently terminated.
        BLOCKED (str): Account is temporarily suspended and cannot perform transactions.
    """

    ACTIVE='active'
    CLOSED='closed'
    BLOCKED='blocked'

class AccountModel(BaseModel):
    """
    Account model representing a user's financial account in the system.
    This model stores information about user accounts including their current balance,
    currency, and status. Each account is associated with a single user and can have
    multiple transactions (both sent and received).
    Attributes:
        user_id (UUID): Foreign key to the user who owns this account.
        balance (Numeric): The current account balance with precision of 10 digits and 3 decimal places.
        currency (VARCHAR): Three-letter currency code, defaults to 'BHD' (Bahraini Dinar).
        account_status (AccountStatus): Current status of the account (e.g., ACTIVE, SUSPENDED).
    Relationships:
        user (UserModel): The user who owns this account.
        sent_transactions (List[TransactionModel]): Transactions where this account is the sender.
        received_transactions (List[TransactionModel]): Transactions where this account is the receiver.
    """

    __tablename__ = 'accounts'
    user_id=Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=False)
    balance =Column(Numeric(precision=10, scale=3), nullable=False, default=0.000)
    currency =Column(VARCHAR(3), nullable=False, default='BHD')
    account_status = Column(SQLAlchemyEnum(AccountStatus), nullable=False, default=AccountStatus.ACTIVE)
    user=relationship('UserModel',back_populates='account')
    sent_transactions = relationship(
        'TransactionModel',
        back_populates='sender_account',
        foreign_keys='TransactionModel.sender_account_id'
    )
    received_transactions = relationship(
        'TransactionModel',
        back_populates='receiver_account',
        foreign_keys='TransactionModel.receiver_account_id'
    )
