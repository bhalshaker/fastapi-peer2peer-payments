from fastapi import APIRouter, Depends, HTTPException
from models import UserModel
from controllers import get_current_user
from schema import UserInfoSchema

user_router = APIRouter()

#Get current user’s profile
@user_router.get(path="/users/me",summary="Get current user’s profile",description="Returns username, email, and account ID",
                 response_model=UserInfoSchema)
async def display_logged_in_userinfo(current_user: UserModel = Depends(get_current_user)):
    """
    Retrieves the profile information of the currently logged-in user.
    
    Args:
        current_user (UserModel): The currently authenticated user model instance.
        
    Returns:
        UserInfoSchema: The schema containing the user's profile information.
        
    Raises:
        HTTPException: If the user is not authenticated or if there is an error retrieving the user information.
    """
    try:
        return UserInfoSchema(username=current_user.username, email=current_user.email, account_id=current_user.account.id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user information: {str(e)}")