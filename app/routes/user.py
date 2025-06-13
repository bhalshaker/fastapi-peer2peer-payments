from fastapi import APIRouter, Depends, HTTPException

user_router = APIRouter()

#Get current user’s profile
@user_router.get(path="/users/me",summary="Get current user’s profile",description="Returns username, email, and account ID")
async def get_current_user(d):
    pass