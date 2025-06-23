from fastapi import APIRouter, Depends, HTTPException
from models import UserModel
from controllers import GetCurrentUserController
from schema import UserInfoSchema

user_router = APIRouter()

#Get current user's profile
@user_router.get("/api/v1/users/me",
                 response_model=UserInfoSchema,
                 summary="Get current user's profile",
                 description="Returns username, email, and account ID")
async def display_logged_in_userinfo(current_user: UserModel = Depends(GetCurrentUserController)):
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

        account_id = None if current_user.account is None else current_user.account.id
        return UserInfoSchema(
            id=current_user.id,
            username=current_user.username, 
            email=current_user.email,
            first_name=current_user.first_name,
            middle_name=current_user.middle_name,
            last_name=current_user.last_name,
            is_admin=current_user.is_admin,
            account_id=account_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving user information: {str(e)}")
