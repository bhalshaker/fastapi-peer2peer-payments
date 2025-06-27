import pytest
from uuid import uuid4
from config import config

test_cases={
        "first_user":{
        "username": "coolcat23",
        "email": "coolcat23@example.com",
        "plain_password": "supersecretpassword1",
        "first_name": "Ahmed",
        "middle_name": "Ali",
        "last_name": "Al-Fulan",
        "account_currency": "bhd"
    },
        "second_user":{
        "username": "coolcat24",
        "email": "coolcat24@example.com",
        "plain_password": "supersecretpassword2",
        "first_name": "Fatima",
        "middle_name": "Ali",
        "last_name": "Al-Fulan",
        "account_currency": "usd"
    },
    "third_user":{
    "username": "michaelmiller",
    "email": "michaelmiller@example.com",
    "plain_password": "XmLvJ80tV@",
    "first_name": "Michael",
    "last_name": "Miller",
    "account_currency": "bhd"
    },
    "fourth_user":{
    "username": "mikewilliams",
    "email": "mikewilliams@example.com",
    "plain_password": "fp1gczr9u#",
    "first_name": "Mike",
    "middle_name": "John",
    "last_name": "Williams",
    "account_currency": "qar"
  },
  "fifth_user":{
    "username": "emilyjones",
    "email": "emilyjones@example.com",
    "plain_password": "Kc7Qdsf0#",
    "first_name": "Emily",
    "middle_name": "Anne",
    "last_name": "Jones",
    "account_currency": "sar"
  },
  "sixth_user":{
    "username": "lindaharris",
    "email": "lindaharris@example.com",
    "plain_password": "Xgb3pYsK*",
    "first_name": "Linda",
    "middle_name": "Marie",
    "last_name": "Harris",
    "account_currency": "kwd"
  },
    "seventh_user":{
    "username": "jacksonsmith",
    "email": "jacksonsmith@example.com",
    "plain_password": "9z9tnLz@1",
    "first_name": "Jackson",
    "last_name": "Smith",
    "account_currency": "bhd"
  },
  "eighth_user":{
    "username": "sarahbrown",
    "email": "sarahbrown@example.com",
    "plain_password": "XfMb%r5Dp1",
    "first_name": "Sarah",
    "middle_name": "Elizabeth",
    "last_name": "Brown",
    "account_currency": "bhd"
  },
  "ninth_user":{
    "username": "jacobdavis",
    "email": "jacobdavis@example.com",
    "plain_password": "bX53LgJH!",
    "first_name": "Jacob",
    "last_name": "Davis",
    "account_currency": "bhd"
  },
    "tenth_user":{
    "username": "katejohnson",
    "email": "katejohnson@example.com",
    "plain_password": "LmnxX92@H",
    "first_name": "Kate",
    "last_name": "Johnson",
    "account_currency": "bhd"
  },
  "eleventh_user":{
    "username": "williamthomas",
    "email": "williamthomas@example.com",
    "plain_password": "b0jRjx73#",
    "first_name": "William",
    "middle_name": "David",
    "last_name": "Thomas",
    "account_currency": "bhd"
  },
  "twelfth_user":{
    "username": "isabellaclark",
    "email": "isabellaclark@example.com",
    "plain_password": "Nt!X29Km0",
    "first_name": "Isabella",
    "last_name": "Clark",
    "account_currency": "USD"
  },
    "first_user_account_top_up":{
        "amount": 500.00
    }
}

# Create a transaction with non-existing receiver account
@pytest.mark.anyio
async def test_create_transaction_with_non_existing_receiver_account(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Prepare transaction request with non-existing receiver account id
    tranasction_request = {
        "receiver_account_id": str(uuid4()),  # Non-existing account ID
        "amount": 100.00
    }
    # Create transaction
    transaction_resp = await client.post("/api/v1/transactions/send", json=tranasction_request,
                                         headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_resp.status_code == 404 # Not Found: The receiver account does not exist.

# Create a successfull transaction
@pytest.mark.anyio
async def test_create_a_successful_transaction(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Create second user
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 100.00
    }
    # Create transaction
    transaction_resp = await client.post("/api/v1/transactions/send", json=tranasction_request,
                                         headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_resp.status_code == 200
    transaction_data = transaction_resp.json()
    assert transaction_data["sender_account_id"] == first_user_data["account_id"]
    assert transaction_data["receiver_account_id"] == second_user_account_id
    assert transaction_data["amount"] == tranasction_request["amount"]
    assert transaction_data["from_currency"] == test_cases["first_user"]["account_currency"]
    assert transaction_data["to_currency"] == test_cases["second_user"]["account_currency"]
    assert transaction_data["status"] == "completed"
    assert transaction_data["exchange_rate"] > 0
    # Check first user account balance
    first_user_account_resp = await client.get("/api/v1/accounts/me",
                                               headers={"Authorization": f"Bearer {first_user_token}"})
    first_user_account_data = first_user_account_resp.json()
    assert first_user_account_data["balance"] == 400.00  # 500 - 100
    # Second user login
    second_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["second_user"]["username"],
        "password": test_cases["second_user"]["plain_password"]
    })
    second_user_login_data = second_user_login_resp.json()
    second_user_token = second_user_login_data['apikey']
    # Check second user account balance
    second_user_account_resp = await client.get("/api/v1/accounts/me",
                                               headers={"Authorization": f"Bearer {second_user_token}"})
    second_user_account_data = second_user_account_resp.json()
    assert second_user_account_data["balance"] >0

# Insuffecient balance transaction
@pytest.mark.anyio
async def test_create_transaction_with_insufficient_balance(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Create second user
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 100.00
    }
    # Create transaction
    transaction_resp = await client.post("/api/v1/transactions/send", json=tranasction_request,
                                         headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_resp.status_code == 406 #Insufficient balance for the transaction.

# ٍSend money to the same account
@pytest.mark.anyio
async def test_send_money_to_the_same_account(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Prepare transaction request
    tranasction_request = {
        "receiver_account_id": first_user_data["account_id"],
        "amount": 100.00
    }
    # Create transaction
    transaction_resp = await client.post("/api/v1/transactions/send", json=tranasction_request,
                                         headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_resp.status_code == 400 #Cannot transfer money to the same account.
# Unauthorized user transaction
@pytest.mark.anyio
async def test_unauthorized_user_transaction(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Create second user
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    # Prepare transaction request
    tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 100.00
    }
    # Create transaction without authorization header
    transaction_resp = await client.post("/api/v1/transactions/send", json=tranasction_request)
    assert transaction_resp.status_code == 403

# Get transaction history of a user
@pytest.mark.anyio
async def test_new_account_without_transactions(client):
    # Create first user
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Get transaction history
    transaction_history_resp = await client.get("/api/v1/transactions/history",
                                                headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 0

# Get transaction history of a user with transactions
@pytest.mark.anyio
async def test_get_transaction_history_of_a_user_with_transactions(client):
    # Create users from first to sixth
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    third_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["third_user"])
    third_user_data = third_user_resp.json()
    third_user_account_id = third_user_data["account_id"]
    fourth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fourth_user"])
    fourth_user_data = fourth_user_resp.json()
    fourth_user_account_id = fourth_user_data["account_id"]
    fifth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fifth_user"])
    fifth_user_data = fifth_user_resp.json()
    fifth_user_account_id = fifth_user_data["account_id"]
    sixth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["sixth_user"])
    sixth_user_data = sixth_user_resp.json()
    sixth_user_account_id = sixth_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Second user login and generate token
    second_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["second_user"]["username"],
        "password": test_cases["second_user"]["plain_password"]
    })
    second_user_login_data = second_user_login_resp.json()
    second_user_token = second_user_login_data['apikey']
    # Third user login and generate token
    third_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["third_user"]["username"],
        "password": test_cases["third_user"]["plain_password"]
    })
    third_user_login_data = third_user_login_resp.json()
    third_user_token = third_user_login_data['apikey']
    # Fourth user login and generate token
    fourth_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["fourth_user"]["username"],
        "password": test_cases["fourth_user"]["plain_password"]
    })
    fourth_user_login_data = fourth_user_login_resp.json()
    fourth_user_token = fourth_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Create transactions
    first_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 10
    }
    second_tranasction_request = {
        "receiver_account_id": third_user_account_id,
        "amount": 20
    }
    third_tranasction_request = {
        "receiver_account_id": fourth_user_account_id,
        "amount": 30
    }
    fourth_tranasction_request = {
        "receiver_account_id": fifth_user_account_id,
        "amount": 40
    }
    fifth_tranasction_request = {
        "receiver_account_id": sixth_user_account_id,
        "amount": 50
    }
    sixth_tramsaction_request = {
        "receiver_account_id": first_user_data["account_id"],
        "amount": 5
    }
    seventh_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 15
    }
    # create first transaction from fist to second user
    first_transaction_resp = await client.post("/api/v1/transactions/send", json=first_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
   # create second transaction from first to third user
    second_transaction_resp = await client.post("/api/v1/transactions/send", json=second_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create third transaction from first to fourth user
    third_transaction_resp = await client.post("/api/v1/transactions/send", json=third_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fourth transaction from first to fifth user
    fourth_transaction_resp = await client.post("/api/v1/transactions/send", json=fourth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fifth transaction from first to sixth user
    fifth_transaction_resp = await client.post("/api/v1/transactions/send", json=fifth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create sixth transaction from second to first user
    sixth_transaction_resp = await client.post("/api/v1/transactions/send", json=sixth_tramsaction_request,
                                                  headers={"Authorization": f"Bearer {second_user_token}"})
    # create seventh transaction from third to second user
    seventh_transaction_resp = await client.post("/api/v1/transactions/send", json=seventh_tranasction_request,
                                                  headers={"Authorization": f"Bearer {third_user_token}"})
    # Check first user transaction history
    transaction_history_resp = await client.get("/api/v1/transactions/history",
                                                headers={"Authorization": f"Bearer {first_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 6
    # Check second user transaction history
    transaction_history_resp = await client.get("/api/v1/transactions/history",
                                                headers={"Authorization": f"Bearer {second_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 3
    # Check third user transaction history
    transaction_history_resp = await client.get("/api/v1/transactions/history",
                                                headers={"Authorization": f"Bearer {third_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 2
    # Check fourth user transaction history
    transaction_history_resp = await client.get("/api/v1/transactions/history",
                                                headers={"Authorization": f"Bearer {fourth_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 1

# Get transaction history of a user with transactions using admin user
@pytest.mark.anyio
async def test_get_transaction_history_of_a_user_with_transactions_using_admin(client, create_admin_user):
    # Create users from first to sixth
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    third_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["third_user"])
    third_user_data = third_user_resp.json()
    third_user_account_id = third_user_data["account_id"]
    fourth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fourth_user"])
    fourth_user_data = fourth_user_resp.json()
    fourth_user_account_id = fourth_user_data["account_id"]
    fifth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fifth_user"])
    fifth_user_data = fifth_user_resp.json()
    fifth_user_account_id = fifth_user_data["account_id"]
    sixth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["sixth_user"])
    sixth_user_data = sixth_user_resp.json()
    sixth_user_account_id = sixth_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Second user login and generate token
    second_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["second_user"]["username"],
        "password": test_cases["second_user"]["plain_password"]
    })
    second_user_login_data = second_user_login_resp.json()
    second_user_token = second_user_login_data['apikey']
    # Third user login and generate token
    third_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["third_user"]["username"],
        "password": test_cases["third_user"]["plain_password"]
    })
    third_user_login_data = third_user_login_resp.json()
    third_user_token = third_user_login_data['apikey']
    # admin user login and generate token
    admin_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": config.admin_username,
        "password": config.admin_password
    })
    admin_user_login_data = admin_user_login_resp.json()
    admin_user_token = admin_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Create transactions
    first_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 10
    }
    second_tranasction_request = {
        "receiver_account_id": third_user_account_id,
        "amount": 20
    }
    third_tranasction_request = {
        "receiver_account_id": fourth_user_account_id,
        "amount": 30
    }
    fourth_tranasction_request = {
        "receiver_account_id": fifth_user_account_id,
        "amount": 40
    }
    fifth_tranasction_request = {
        "receiver_account_id": sixth_user_account_id,
        "amount": 50
    }
    sixth_tramsaction_request = {
        "receiver_account_id": first_user_data["account_id"],
        "amount": 5
    }
    seventh_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 15
    }
    # create first transaction from fist to second user
    first_transaction_resp = await client.post("/api/v1/transactions/send", json=first_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
   # create second transaction from first to third user
    second_transaction_resp = await client.post("/api/v1/transactions/send", json=second_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create third transaction from first to fourth user
    third_transaction_resp = await client.post("/api/v1/transactions/send", json=third_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fourth transaction from first to fifth user
    fourth_transaction_resp = await client.post("/api/v1/transactions/send", json=fourth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fifth transaction from first to sixth user
    fifth_transaction_resp = await client.post("/api/v1/transactions/send", json=fifth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create sixth transaction from second to first user
    sixth_transaction_resp = await client.post("/api/v1/transactions/send", json=sixth_tramsaction_request,
                                                  headers={"Authorization": f"Bearer {second_user_token}"})
    # create seventh transaction from third to second user
    seventh_transaction_resp = await client.post("/api/v1/transactions/send", json=seventh_tranasction_request,
                                                  headers={"Authorization": f"Bearer {third_user_token}"})
    # Check first user transaction history
    transaction_history_resp = await client.get(f"/api/v1/transactions/{first_user_data['id']}",
                                                headers={"Authorization": f"Bearer {admin_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 6
    # Check second user transaction history
    transaction_history_resp = await client.get(f"/api/v1/transactions/{second_user_data['id']}",
                                                headers={"Authorization": f"Bearer {admin_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 3
    # Check third user transaction history
    transaction_history_resp = await client.get(f"/api/v1/transactions/{third_user_data['id']}",
                                                headers={"Authorization": f"Bearer {admin_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 2
    # Check fourth user transaction history
    transaction_history_resp = await client.get(f"/api/v1/transactions/{fourth_user_data['id']}",
                                                headers={"Authorization": f"Bearer {admin_user_token}"})
    assert transaction_history_resp.status_code == 200
    transaction_history_data = transaction_history_resp.json()
    assert isinstance(transaction_history_data['transactions'], list)
    assert len(transaction_history_data['transactions']) == 1

# Fail to get transaction history of a user with transactions using non-admin user
@pytest.mark.anyio
async def test_fail_to_get_transaction_history_of_a_user_with_transactions_using_non_admin(client):
    # Create users from first to sixth
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    third_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["third_user"])
    third_user_data = third_user_resp.json()
    third_user_account_id = third_user_data["account_id"]
    fourth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fourth_user"])
    fourth_user_data = fourth_user_resp.json()
    fourth_user_account_id = fourth_user_data["account_id"]
    fifth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["fifth_user"])
    fifth_user_data = fifth_user_resp.json()
    fifth_user_account_id = fifth_user_data["account_id"]
    sixth_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["sixth_user"])
    sixth_user_data = sixth_user_resp.json()
    sixth_user_account_id = sixth_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Second user login and generate token
    second_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["second_user"]["username"],
        "password": test_cases["second_user"]["plain_password"]
    })
    second_user_login_data = second_user_login_resp.json()
    second_user_token = second_user_login_data['apikey']
    # Third user login and generate token
    third_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["third_user"]["username"],
        "password": test_cases["third_user"]["plain_password"]
    })
    third_user_login_data = third_user_login_resp.json()
    third_user_token = third_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Create transactions
    first_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 10
    }
    second_tranasction_request = {
        "receiver_account_id": third_user_account_id,
        "amount": 20
    }
    third_tranasction_request = {
        "receiver_account_id": fourth_user_account_id,
        "amount": 30
    }
    fourth_tranasction_request = {
        "receiver_account_id": fifth_user_account_id,
        "amount": 40
    }
    fifth_tranasction_request = {
        "receiver_account_id": sixth_user_account_id,
        "amount": 50
    }
    sixth_tramsaction_request = {
        "receiver_account_id": first_user_data["account_id"],
        "amount": 5
    }
    seventh_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 15
    }
    # create first transaction from fist to second user
    first_transaction_resp = await client.post("/api/v1/transactions/send", json=first_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
   # create second transaction from first to third user
    second_transaction_resp = await client.post("/api/v1/transactions/send", json=second_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create third transaction from first to fourth user
    third_transaction_resp = await client.post("/api/v1/transactions/send", json=third_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fourth transaction from first to fifth user
    fourth_transaction_resp = await client.post("/api/v1/transactions/send", json=fourth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create fifth transaction from first to sixth user
    fifth_transaction_resp = await client.post("/api/v1/transactions/send", json=fifth_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create sixth transaction from second to first user
    sixth_transaction_resp = await client.post("/api/v1/transactions/send", json=sixth_tramsaction_request,
                                                  headers={"Authorization": f"Bearer {second_user_token}"})
    # create seventh transaction from third to second user
    seventh_transaction_resp = await client.post("/api/v1/transactions/send", json=seventh_tranasction_request,
                                                  headers={"Authorization": f"Bearer {third_user_token}"})
    # Check first user transaction history using second user token
    transaction_history_resp = await client.get(f"/api/v1/transactions/{first_user_data['id']}",
                                                headers={"Authorization": f"Bearer {second_user_token}"})
    assert transaction_history_resp.status_code == 401 # Unauthorized: Only admin users can access this endpoint.

# Fail to get transaction history of a non existing user with transactions using an admin user
@pytest.mark.anyio
async def test_fail_to_get_transaction_history_of_a_non_existing_user_with_transactions_using_admin(client, create_admin_user):
    # Create users from first to Third
    first_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["first_user"])
    first_user_data = first_user_resp.json()
    second_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["second_user"])
    second_user_data = second_user_resp.json()
    second_user_account_id = second_user_data["account_id"]
    third_user_resp=await client.post("/api/v1/auth/signup", json=test_cases["third_user"])
    third_user_data = third_user_resp.json()
    third_user_account_id = third_user_data["account_id"]
    # Login first user and generate token
    first_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["first_user"]["username"],
        "password": test_cases["first_user"]["plain_password"]
    })
    first_user_login_data = first_user_login_resp.json()
    first_user_token = first_user_login_data['apikey']
    # Second user login and generate token
    second_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["second_user"]["username"],
        "password": test_cases["second_user"]["plain_password"]
    })
    second_user_login_data = second_user_login_resp.json()
    second_user_token = second_user_login_data['apikey']
    # Third user login and generate token
    third_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": test_cases["third_user"]["username"],
        "password": test_cases["third_user"]["plain_password"]
    })
    third_user_login_data = third_user_login_resp.json()
    third_user_token = third_user_login_data['apikey']
    # admin user login and generate token
    admin_user_login_resp = await client.post("/api/v1/auth/login", json={
        "username": config.admin_username,
        "password": config.admin_password
    })
    admin_user_login_data = admin_user_login_resp.json()
    admin_user_token = admin_user_login_data['apikey']
    # Top up first user account
    await client.post("/api/v1/accounts/top-up", json=test_cases["first_user_account_top_up"],
                                    headers={"Authorization": f"Bearer {first_user_token}"})
    # Create transactions
    first_tranasction_request = {
        "receiver_account_id": second_user_account_id,
        "amount": 10
    }
    second_tranasction_request = {
        "receiver_account_id": third_user_account_id,
        "amount": 20
    }
    # create first transaction from fist to second user
    first_transaction_resp = await client.post("/api/v1/transactions/send", json=first_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # create second transaction from first to third user
    second_transaction_resp = await client.post("/api/v1/transactions/send", json=second_tranasction_request,
                                                  headers={"Authorization": f"Bearer {first_user_token}"})
    # Check non ecisting user transaction history using admin user token
    transaction_history_resp = await client.get(f"/api/v1/transactions/{uuid4()}",
                                                headers={"Authorization": f"Bearer {admin_user_token}"})
    assert transaction_history_resp.status_code == 404