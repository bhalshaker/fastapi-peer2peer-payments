from pydantic import BaseModel
from uuid import UUID

class CreateTransactionRequest(BaseModel):
    pass


class TransactionInfoSchema(BaseModel):
    pass

class TransactionsOfUserSchema(BaseModel):
    user_id: UUID
    transactions: list[TransactionInfoSchema]
