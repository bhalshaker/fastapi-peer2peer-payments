from pydantic import BaseModel,PositiveFloat
from uuid import UUID

class CreateTransactionRequestSchema(BaseModel):
    receiver_account_id : UUID
    amount : float


class TransactionInfoSchema(BaseModel):
    sender_account_id : UUID
    receiver_account_id : UUID
    amount : PositiveFloat
    from_currency : str
    to_currency : str
    exchange_rate : float
    status : str

class TransactionsOfUserSchema(BaseModel):
    user_id: UUID
    transactions: list[TransactionInfoSchema]
