from fastapi import APIRouter, Depends, HTTPException

transaction_router = APIRouter()

@transaction_router.post("/api/v1/transactions/send")
async def transfer_money():
    pass

@transaction_router.get("/api/v1/transactions/history")
async def get_transaction_history():
    pass

@transaction_router.get("/api/v1/transactions/{user_id}")
async def get_user_transaction_history(user_id: str):
    pass