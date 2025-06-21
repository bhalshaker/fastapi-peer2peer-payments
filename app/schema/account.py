from pydantic import BaseModel
from uuid import UUID

class CreateAccountSchema(BaseModel):
    """
    Schema for creating a new account.
    """
    user_id:UUID
    currency:str