from pydantic import BaseModel, Field
class ExchangeRate(BaseModel):
    """
    Response model for exchange rate utility.
    """
    exchange_rate: float = Field(..., description="The exchange rate between the two currencies.")
    converted_amount: float = Field(..., description="The amount converted from the from_currency to the to_currency.")