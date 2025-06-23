from datetime import datetime, timedelta,timezone  # New import for timestamps
import jwt  # New import for token generation
from uuid import UUID
from config import config
from schema.token import JWTSchema, PayloadSchema,DecodedTokenSchema

def generate_token(user_id:UUID,is_admin:bool)->JWTSchema:
        """
        Generates a JSON Web Token (JWT) for a given user ID.
        Args:
            id (uuid): The unique identifier of the user for whom the token is generated.
        Returns:
            JWTSchema: The encoded JWT token.
        The token includes the following claims:
            - expires_at: Expiration time (1 day from now)
            - issued_at: Issued at time (current time)
            - subject: Subject (user ID)
            - is_admin: Boolean indicating if the user is an admin
        """
        
        payload = generate_token_payload(user_id, is_admin)
        token = jwt.encode(payload.model_dump(), config.token_secret, algorithm="HS256")
        user_response = JWTSchema(**payload.model_dump(exclude={"sub","is_admin"}), apikey=token)
        return user_response

def decode_token(credentials:str)->DecodedTokenSchema:
        """
        Decodes a JWT token and retrieves the subject ("sub") claim.
        Args:
            token: An object containing the JWT credentials as an attribute.
        Returns:
            DecodedTokenSchema: The subject claim from the decoded JWT payload.
        """
        
        payload = jwt.decode(credentials, config.token_secret, algorithms=["HS256"])
        return DecodedTokenSchema(sub=payload.get("sub"), is_admin=payload.get("is_admin"))

def generate_token_payload(user_id:UUID,is_admin:bool,expiration_time: int = 86400) -> PayloadSchema:
    """
    Generates a token payload with an expiration time.
    Args:
        expiration_time (int): The expiration time in seconds. Default is 86400 seconds (1 day).
    Returns:
        PayloadSchema: The token payload with the expiration time.
    """
    return PayloadSchema(exp=datetime.now(timezone.utc) + timedelta(seconds=expiration_time),
                         iat=datetime.now(timezone.utc),
                         sub=str(user_id),
                         is_admin=is_admin)