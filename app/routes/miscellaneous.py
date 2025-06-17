from fastapi import APIRouter, Depends, HTTPException
from schema import ExchangeRateParameters
from httpx import AsyncClient
from config import config


miscellaneous_router = APIRouter()

@miscellaneous_router.get("/api/v1/exchange-rate")
async def get_exchange_rate(exchange_rate_params: ExchangeRateParameters):
    """
    Get the exchange rate between two currencies.
    """
    from_currency = exchange_rate_params.from_currency.lower()
    to_currency = exchange_rate_params.to_currency.lower()
    
    async with AsyncClient() as client:
        response = await client.get(
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.json"
        )
        
        if response.status_code == 200:
            data = response.json()
            data[from_currency][to_currency]*config.processing_fees
        else:
            raise HTTPException(status_code=response.status_code, detail="Error fetching exchange rate")