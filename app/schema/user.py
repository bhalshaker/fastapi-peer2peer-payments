from typing import Optional
from pydantic import BaseModel,EmailStr,computed_field
from utilities import hash_a_password

class CreateUserSchema(BaseModel):
    """
    Schema for creating a new user.
    Attributes:
        username (str): The username of the user.
        email (EmailStr): The email address of the user.
        plain_password (str): The plain password for the user account.
        first_name (str): The first name of the user.
        middle_name (Optional[str]): The middle name of the user, optional.
        last_name (str): The last name of the user.
    """
    username: str
    email: EmailStr
    plain_password: str
    first_name: str
    middle_name : Optional[str] = None
    last_name: str

    @computed_field
    @property
    def password(self) -> str:
        """
        Returns the hashed password for the user.
        This is used to create the dnfuser with a hashed password later.
        """
        return hash_a_password(self.plain_password)