from httpx import AsyncClient
from config import config
from functools import cache

async def convert_currency(from_currency: str, to_currency: str, amount: float=1.0) -> float:
    """
    Convert an amount from one currency to another using a mock exchange rate.
    """
    async with AsyncClient() as client:
        response = await client.get(
            f"https://cdn.jsdelivr.net/npm/@fawazahmed0/currency-api@latest/v1/currencies/{from_currency}.json"
        )
        
        if response.status_code == 200:
            data = response.json()
            return data[from_currency][to_currency]*config.processing_fees*amount

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
