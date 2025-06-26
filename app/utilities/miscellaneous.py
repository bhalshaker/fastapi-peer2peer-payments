from httpx import AsyncClient
from config import config
from functools import cache
from tenacity import retry,stop_after_attempt

@retry(stop=stop_after_attempt(3))
async def convert_currency(from_currency: str, to_currency: str, amount: float=1.0) -> dict:
    """
    Convert an amount from one currency to another using a mock exchange rate.
    """
    async with AsyncClient() as client:
        response = await client.get(
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.json"
        )
        
        if response.status_code == 200:
            data = response.json()
            rate=data[from_currency][to_currency]*(1-config.processing_fees)
            converted_amount=rate*amount
            return {"exchange_rate": rate, "converted_amount": converted_amount}

@retry(stop=stop_after_attempt(3))
@cache
async def get_currencies_list() -> list[str]:
    """
    Fetch the list of valid currencies from the API and cache it.
    """
    async with AsyncClient() as client:
        response = await client.get(
            "https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies.json"
        )
        
        if response.status_code == 200:
            data = response.json()
            return list(data.keys())
        else:
            raise Exception("Error fetching currency list")
