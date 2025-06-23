from pydantic import BaseModel,computed_field
from datetime import datetime
from uuid import UUID

class JWTSchema(BaseModel):
    exp:datetime
    iat:datetime
    apikey:str

class PayloadSchema(BaseModel):
    exp:datetime
    iat:datetime
    sub:str
    is_admin:bool

class DecodedTokenSchema(BaseModel):
    sub: str
    is_admin: bool

    @computed_field
    @property
    def user_id(self) -> str:
        """
        Returns the user ID from the subject field.
        """
        return UUID(self.sub)

class TokenResponseSchema(JWTSchema):
    """
    Schema for the token response.
    """
    @computed_field
    @property
    def token_type(self) -> str:
        """
        Returns the type of the token.
        """
        return "Bearer"