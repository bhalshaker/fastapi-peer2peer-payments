from pydantic import BaseModel, Field,field_validator
from controllers import GetCurrenciesListController

class ExchangeRateParameters(BaseModel):
    """
    Parameters for exchange rate conversion.
    """
    from_currency: str = Field(..., alias="from", description="The currency to convert from.")
    to_currency: str = Field(..., alias="to", description="The currency to convert to.")
    
    @field_validator('from_currency', 'to_currency')
    def validate_currency(cls, value: str) -> str:
        """Validate that the currency is in the list of valid currencies."""
        # Cache currencies at class level to avoid repeated calls
        currencies = GetCurrenciesListController()
        if value.lower() not in currencies:
            raise ValueError(f"'{value}' is not a valid currency code")
        return value.lower()  # Normalize to lowercase