from pydantic import BaseModel,PositiveFloat, ValidationError, field_validator
from typing import ClassVar
from uuid import UUID

class CreateAccountSchema(BaseModel):
    """
    Schema for creating a new account.
    """
    user_id:UUID
    currency:str

class AccountInfoSchema(BaseModel):
    """
    Schema for account information.
    """
    user_id:UUID
    account_id:UUID
    balance:float
    currency:str

class TopUpRequestSchema(BaseModel):
    """
    Schema for top-up request.
    """
    amount: PositiveFloat

    @field_validator('amount')
    @classmethod
    def check_value_positive(cls, v: float):
        if not v > 0: # This check is actually redundant for PositiveFloat, but shows the pattern
            raise ValueError('The amount must be a positive number, strictly greater than zero.')
        return v