import pytest
from uuid import uuid4
from utilities import generate_token

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
    "second_user":
    {
        "username": "sunshine_dev",
        "email": "s.dev@example.com",
        "plain_password": "P@ssw0rdPro!",
        "first_name": "Fatima",
        "middle_name": "Zahra",
        "last_name": "Khan",
        "account_currency": "usd"
  },
  "user_failed_currency":
  {
        "username": "failed_currency_user",
        "email": "failed_currency_user@example.com",
        "plain_password": "P@ssw0rdPro!",
        "first_name": "Sameer",
        "middle_name": "Zahid",
        "last_name": "Khan",
        "account_currency": "usa"
  }
}

# Test for successful user creation
@pytest.mark.anyio
async def test_create_transaction_success(client):
    # Create first user
    user_creation_resp=await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Assert user creation was successful
    assert user_creation_resp.status_code == 200
    user_data = user_creation_resp.json()
    # Assert user data matches expected values
    assert user_data["username"] == transaction_test_data["first_user"]["username"]
    assert user_data["email"] == transaction_test_data["first_user"]["email"]
    assert user_data["first_name"] == transaction_test_data["first_user"]["first_name"]
    assert user_data["middle_name"] == transaction_test_data["first_user"]["middle_name"]
    assert user_data["last_name"] == transaction_test_data["first_user"]["last_name"]
    assert 'id' in user_data
    assert 'account_id' in user_data

# Test for user creation with existing username
@pytest.mark.anyio
async def test_create_transaction_existing_username(client):
    # Create first user
    await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Attempt to create a second user with the same username
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Assert user creation failed with 400 Bad Request
    assert user_creation_resp.status_code == 400
    assert user_creation_resp.json() == {"detail": "Username or email already exists."}

# Test for user creation with invalid currency
@pytest.mark.anyio
async def test_create_transaction_invalid_currency(client):
    # Attempt to create a user with an invalid currency
    user_creation_resp = await client.post("/api/v1/auth/signup", json=transaction_test_data["user_failed_currency"])
    # Assert user creation failed with 422 Unprocessable Entity
    assert user_creation_resp.status_code == 422
    #assert user_creation_resp.json() == {"detail": "Invalid currency code. Must be a valid ISO 4217 currency code."}

#Test for sucessful login
@pytest.mark.anyio
async def test_successful_login(client):
    # Create first user
    await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Login with the created user
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    # Assert login was successful
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    # Assert token is present in the response
    assert 'exp' in login_data
    assert 'iat' in login_data
    assert 'apikey' in login_data
    assert 'token_type' in login_data

# Test for failed login with incorrect password
@pytest.mark.anyio
async def test_failed_login_incorrect_password(client):
    # Create first user
    await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Attempt to login with incorrect password
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": "wrongpassword"
    })
    # Assert login failed with 401 Unauthorized
    assert login_resp.status_code == 401
    assert login_resp.json() == {"detail": "Incorrect combination of username and password"}

# Test for failed login with non-existent user
@pytest.mark.anyio
async def test_failed_login_non_existent_user(client):
    # Attempt to login with a non-existent user
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": "non_existent_user",
        "password": "somepassword"
    })
    # Assert login failed with 401 Unauthorized
    assert login_resp.status_code == 401
    assert login_resp.json() == {"detail": "Incorrect combination of username and password"}

#Get current user's profile
@pytest.mark.anyio
async def test_get_current_user_profile(client):
    # Create first user
    await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    # Login with the created user
    login_resp = await client.post("/api/v1/auth/login", json={
        "username": transaction_test_data["first_user"]["username"],
        "password": transaction_test_data["first_user"]["plain_password"]
    })
    # Assert login was successful
    assert login_resp.status_code == 200
    login_data = login_resp.json()
    # Get the token from the login response
    token = login_data['apikey']
    
    # Get current user's profile
    profile_resp = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    # Assert profile retrieval was successful
    assert profile_resp.status_code == 200
    profile_data = profile_resp.json()
    
    # Assert profile data matches expected values
    assert profile_data["username"] == transaction_test_data["first_user"]["username"]
    assert profile_data["email"] == transaction_test_data["first_user"]["email"]
    assert profile_data["first_name"] == transaction_test_data["first_user"]["first_name"]
    assert profile_data["middle_name"] == transaction_test_data["first_user"]["middle_name"]
    assert profile_data["last_name"] == transaction_test_data["first_user"]["last_name"]
    assert 'id' in profile_data
    assert 'account_id' in profile_data

# Test for getting current user's profile without authentication
@pytest.mark.anyio
async def test_get_current_user_profile_unauthenticated(client):
    # Attempt to get current user's profile without authentication
    profile_resp = await client.get("/api/v1/users/me")
    # Assert profile retrieval failed with 401 Unauthorized
    assert profile_resp.status_code == 403
    assert profile_resp.json() == {"detail": "Not authenticated"}

# Test for getting current user's profile with invalid token
@pytest.mark.anyio
async def test_get_current_user_profile_invalid_token(client):
    # Create first user
    await client.post("/api/v1/auth/signup", json=transaction_test_data["first_user"])
    
    # Get current user's profile with an invalid token
    profile_resp = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": "Bearer invalid_token"}
    )
    
    # Assert profile retrieval failed with 401 Unauthorized
    assert profile_resp.status_code == 401

#Not a valid user id token
@pytest.mark.anyio
async def test_get_current_user_profile_invalid_user_id(client):
    token_json=generate_token(uuid4(),False) 
    # Get current user's profile with an invalid user ID token
    profile_resp = await client.get(
        "/api/v1/users/me",
        headers={"Authorization": f"Bearer {token_json.apikey}"})
    
    # Assert profile retrieval failed with 401 Unauthorized
    assert profile_resp.status_code == 401