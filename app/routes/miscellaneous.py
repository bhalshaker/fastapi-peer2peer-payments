from fastapi import APIRouter, Depends, HTTPException, Query
from schema import ExchangeRateParameters
from utilities import ConvertCurrencyController, GetCurrenciesListController


miscellaneous_router = APIRouter()

@miscellaneous_router.get("/api/v1/exchange-rate")
async def get_exchange_rate(
    from_currency: str = Query(alias="from", description="The currency to convert from.",title="From Currency"),
    to_currency: str = Query(alias="to",description="The currency to convert to.", title="To Currency")
):
    """
    Get the exchange rate between two currencies.
    """
    # Normalize to lowercase
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()
    
    try:
        # Validate that the currencies are valid
        currencies = await GetCurrenciesListController()
        if from_currency not in currencies:
            raise HTTPException(status_code=400, detail=f"Invalid currency code: {from_currency}")
        if to_currency not in currencies:
            raise HTTPException(status_code=400, detail=f"Invalid currency code: {to_currency}")
        
        # Convert the currency
        rate = await ConvertCurrencyController(from_currency, to_currency)
        return {"from": from_currency, "to": to_currency, "rate": rate}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    