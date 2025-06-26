import pytest

transaction_test_data={
    "first_user":
    {
        "username": "coolcat23",
        "email": "coolcat23@example.com",
        "plain_password": "supersecretpassword1",
        "first_name": "Ahmed",
        "middle_name": "Ali",
        "last_name": "Al-Fulan",
        "account_currency": "bhd"
    },
    "update_account":
    {
        "amount": 500.325
    },
    "failed_update_account":
    {
        "amount": -100.00 
    }

}

# Successfully get user account details
@pytest.mark.anyio
async def test_check_newly_created_user_account_details(client):
    # Create first user
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Assert user creation was successful
    assert user_creation_resp.status_code == 200
    user_data = user_creation_resp.json()
    
    # Check if account details are present
    assert 'account_id' in user_data
    #  login and generate token
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data['apikey']
    account_details_resp = await client.get(f"/api/v1/accounts/me",headers={"Authorization": f"Bearer {token}"})
    assert account_details_resp.status_code == 200
    account_data = account_details_resp.json()
    # Assert account details match expected values
    assert account_data["user_id"] == user_data["id"]
    assert account_data["account_id"] == user_data["account_id"]
    assert account_data["currency"] == transaction_test_data["first_user"]["account_currency"]
    assert account_data["balance"] == 0.0  # New account should have zero

# Successfully top up user account
@pytest.mark.anyio
async def test_top_up_account(client):
    # Create first user
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    assert user_creation_resp.status_code == 200
    user_data = user_creation_resp.json()
    
    # Login and generate token
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data['apikey']
    
    # Top up account
    top_up_resp = await client.post(f"/api/v1/accounts/top-up", json=transaction_test_data["update_account"], headers={"Authorization": f"Bearer {token}"})
    assert top_up_resp.status_code == 200
    top_up_data = top_up_resp.json()
    
    # Assert the balance is updated correctly
    assert top_up_data["balance"] == transaction_test_data["update_account"]["amount"]

# Fail to top up account with invalid amount
@pytest.mark.anyio
async def test_top_up_account(client):
    # Create first user
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    assert user_creation_resp.status_code == 200
    user_data = user_creation_resp.json()
    
    # Login and generate token
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data['apikey']
    
    # Top up account
    top_up_resp = await client.post(f"/api/v1/accounts/top-up", json=transaction_test_data["failed_update_account"], headers={"Authorization": f"Bearer {token}"})
    assert top_up_resp.status_code == 422

# Failed to update due to invalid token
@pytest.mark.anyio
async def test_top_up_account(client):
    # Create first user
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    assert user_creation_resp.status_code == 200
    user_data = user_creation_resp.json()
    
    # Login and generate token
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    token = login_data['apikey']+"1"
    
    # Top up account
    top_up_resp = await client.post(f"/api/v1/accounts/top-up", json=transaction_test_data["update_account"], headers={"Authorization": f"Bearer {token}"})
    assert top_up_resp.status_code == 401