from enum import Enum
from .base import BaseModel
from sqlalchemy import Column, Enum as SQLAlchemyEnum,UUID,ForeignKey,Numeric,VARCHAR
from sqlalchemy.orm import relationship

class TransactionStatus(Enum):
    """
    Enum representing the status of a transaction in the payment system.
    Attributes:
        PENDING (str): Transaction has been initiated but not yet finalized.
                      The funds are reserved but not transferred.
        COMPLETED (str): Transaction has been successfully processed and finalized.
                        The funds have been transferred to the recipient.
        FAILED (str): Transaction could not be completed due to an error or rejection.
                     No funds were transferred.
    """

    PENDING = 'pending'
    COMPLETED = 'completed'
    FAILED = 'failed'

class TransactionModel(BaseModel):
    """
    Represents a financial transaction between two accounts in the peer-to-peer payment system.
    This model tracks money transfers between accounts, including currency conversion details
    and the current status of the transaction.
    Attributes:
        sender_account_id (UUID): Identifier of the account sending the funds.
        receiver_account_id (UUID): Identifier of the account receiving the funds.
        amount (Numeric): The transaction amount with up to 3 decimal places.
        from_currency (VARCHAR): 3-letter currency code of the sender's currency.
        to_currency (VARCHAR): 3-letter currency code of the receiver's currency.
        exchange_rate (Numeric): The currency conversion rate used for the transaction,
                                with up to 6 decimal places. Defaults to 1.0.
        status (TransactionStatus): Current status of the transaction (e.g., PENDING, 
                                   COMPLETED, FAILED). Defaults to PENDING.
        sender_account (relationship): Relationship to the account that sent the funds.
        receiver_account (relationship): Relationship to the account that received the funds.
    """

    __tablename__ = 'transactions'
    
    sender_account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    receiver_account_id = Column(UUID(as_uuid=True), ForeignKey('accounts.id'), nullable=False)
    amount = Column(Numeric(precision=10, scale=3), nullable=False, default=0.000)
    from_currency = Column(VARCHAR(3), nullable=False)
    to_currency = Column(VARCHAR(3), nullable=False)
    exchange_rate = Column(Numeric(precision=10, scale=6), nullable=False, default=1.000000)
    status = Column(SQLAlchemyEnum(TransactionStatus), nullable=False, default=TransactionStatus.PENDING)
    sender_account = relationship('AccountModel', back_populates='sent_transactions', foreign_keys=[sender_account_id])
    receiver_account = relationship('AccountModel', back_populates='received_transactions', foreign_keys=[receiver_account_id])