from fastapi import APIRouter, Depends, HTTPException, Query,Request
from schema import ExchangeRateParameters,ExchangeRateRespsonse
from utilities import ConvertCurrencyController, GetCurrenciesListController


miscellaneous_router = APIRouter()
_currencies_cache = None

async def get_currencies_list():
    global _currencies_cache
    if _currencies_cache is None:
        _currencies_cache = await GetCurrenciesListController()

@miscellaneous_router.get("/api/v1/exchange-rate",summary="Get Exchange Rate",
    description="Get the exchange rate between two currencies.",
    response_model=ExchangeRateRespsonse)
async def get_exchange_rate(request: Request,
    from_currency: str = Query(alias="from", description="The currency to convert from.",title="From Currency"),
    to_currency: str = Query(alias="to",description="The currency to convert to.", title="To Currency")
):
    """
    Get the exchange rate between two currencies.
    """
    print(f"Request received for exchange rate from {from_currency} to {to_currency}")
    allowed_params={"from", "to"}
    actual_params = set(request.query_params.keys())
    extra_params = actual_params - allowed_params
    if extra_params:
        raise HTTPException(status_code=422, detail=f"Invalid query parameters: {', '.join(extra_params)}")
    if not from_currency or not to_currency:
        raise HTTPException(status_code=422, detail="Both 'from' and 'to' parameters are required.")
    # Normalize to lowercase
    from_currency = from_currency.lower()
    to_currency = to_currency.lower()
    
    try:
        # Validate that the currencies are valid
        await get_currencies_list()
        if from_currency not in _currencies_cache:
            raise HTTPException(status_code=422, detail=f"Invalid currency code: {from_currency}")
        if to_currency not in _currencies_cache:
            raise HTTPException(status_code=422, detail=f"Invalid currency code: {to_currency}")
        
        # Convert the currency
        rate = await ConvertCurrencyController(from_currency, to_currency)
        exchange_response = ExchangeRateRespsonse(from_currency=from_currency, to_currency=to_currency, rate=round(rate,3))
        return exchange_response
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    