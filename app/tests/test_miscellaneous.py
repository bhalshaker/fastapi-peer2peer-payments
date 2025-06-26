import pytest

# Test with lowercase currencies
@pytest.mark.anyio
async def test_get_exchange_rate_lowercase_currencies(client):
    response = await client.get("/api/v1/exchange-rate?from=usd&to=bhd")
    assert response.status_code == 200
    data = response.json()
    assert data["from_currency"] == "usd"
    assert data["to_currency"] == "bhd"
    assert data["rate"] == 0.372
    assert data["converted_amount"] == 0.37224

# Test with uppercase currencies
@pytest.mark.anyio
async def test_get_exchange_rate_uppercase_currencies(client):
    response = await client.get("/api/v1/exchange-rate?from=USD&to=BHD")
    assert response.status_code == 200
    data = response.json()
    assert data["from_currency"] == "usd"
    assert data["to_currency"] == "bhd"
    assert data["rate"] == 0.372
    assert data["converted_amount"] == 0.37224

# Test with wrong currency codes
@pytest.mark.anyio
async def test_get_exchange_rate_invalid_currency(client):
    response = await client.get("/api/v1/exchange-rate?from=XXX&to=YYY")
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data