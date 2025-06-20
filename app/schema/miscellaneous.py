from pydantic import BaseModel, Field, field_serializer
from typing import Annotated
from fastapi import Query

class ExchangeRateParameters(BaseModel):
    """
    Parameters for exchange rate conversion.
    """
    from_currency: str = Field(..., description="The currency to convert from.")
    to_currency: str = Field(..., description="The currency to convert to.")
    
    model_config = {
        "populate_by_name": True
    }
    
    # @field_validator('from_currency', 'to_currency')
    # def validate_currency(cls, value: str) -> str:
    #     """Validate that the currency is in the list of valid currencies."""
    #     # Don't validate - we'll just normalize to lowercase
    #     # Actual API validation will happen when the endpoint is called
    #     return value.lower()  # Normalize to lowercase