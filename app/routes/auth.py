from fastapi import APIRouter, Depends, HTTPException

auth_router = APIRouter()

@auth_router.post("/api/v1/auth/login")
async def login():
    pass

@auth_router.post("/api/v1/auth/signup")
async def signup():
    pass