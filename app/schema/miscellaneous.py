from pydantic import BaseModel, Field, field_serializer

class ExchangeRateRespsonse(BaseModel):
    """
    Response model for exchange rate conversion.
    """
    from_currency: str = Field(..., description="The currency converted from.")
    to_currency: str = Field(..., description="The currency converted to.")
    rate: float = Field(..., description="The exchange rate between the two currencies.")
    converted_amount: float = Field(..., description="The amount converted from the from_currency to the to_currency.")

