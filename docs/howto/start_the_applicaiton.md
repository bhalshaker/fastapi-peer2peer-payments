# Start the application

## Prerequesits

* Make sure that you can have cloned the project and configured env correctly and you are currently in the project cloned folder.
* Make sure that you have a posgresql server running and have created a database.
* Make sure that you have an access to the postgresql server and the internet to call the external APIs.
* Make sure that you have .env file in place with correct settings

## Seed the application

This will make a fresh database schema for the application and setup the admin user based on .env configuration

```sh
python app/seed.py
```

## Start application
* get into app folder
```sh
cd app
```
* Start fastapi using uvicorn
```sh
uvicorn main:app
```

* Open swagger UI and start using the application most likely the URL will be http://localhost:8000/docs

## An exhibit of using the running application using CURL

Below are some examples of how to use the Peer2Peer Payments API with curl commands. These examples demonstrate key functionality based on our transaction history and exchange rate tests.

### Authentication

First, create a new user account:

```sh
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "coolcat23",
    "email": "coolcat23@example.com",
    "plain_password": "supersecretpassword1",
    "first_name": "Ahmed",
    "middle_name": "Ali",
    "last_name": "Al-Fulan",
    "account_currency": "bhd"
  }'
```

Then login to obtain an API key:

```sh
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "coolcat23",
    "password": "supersecretpassword1"
  }'
```

Save the returned `apikey` for use in subsequent requests:

```sh
# Store the API key in a variable for convenience
export API_KEY="your_received_apikey_here"
```

### Account Operations

Top up your account balance:

```sh
curl -X POST http://localhost:8000/api/v1/accounts/top-up \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 500.00
  }'
```

Check your account balance:

```sh
curl -X GET http://localhost:8000/api/v1/accounts/me \
  -H "Authorization: Bearer $API_KEY"
```

### Currency Exchange Rates

Get currency exchange rate information:

```sh
curl -X GET "http://localhost:8000/api/v1/exchange-rate?from=usd&to=bhd" \
  -H "Authorization: Bearer $API_KEY"
```

The response will include the conversion rate and the converted amount (for 1 unit):

```json
{
  "from_currency": "usd",
  "to_currency": "bhd",
  "rate": 0.372,
  "converted_amount": 0.37224
}
```

### Transactions

Send money to another user (you need their account ID):

```sh
curl -X POST http://localhost:8000/api/v1/transactions/send \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "receiver_account_id": "recipient_account_id_here",
    "amount": 100.00
  }'
```

View your transaction history:

```sh
curl -X GET http://localhost:8000/api/v1/transactions/history \
  -H "Authorization: Bearer $API_KEY"
```

### Admin Operations

If you have admin privileges, you can view transaction history for any user:

```sh
# First, login as admin
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "audit_admin",
    "password": "admin_password"
  }'

# Store the admin API key
export ADMIN_API_KEY="admin_apikey_here"

# View a specific user's transactions using their user ID
curl -X GET "http://localhost:8000/api/v1/transactions/user_id_here" \
  -H "Authorization: Bearer $ADMIN_API_KEY"
```
