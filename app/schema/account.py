from pydantic import BaseModel

class CreateAccountSchema(BaseModel):
    """
    Schema for creating a new account.
    """
    username: str
    email: str
    password: str
    is_admin: bool = False