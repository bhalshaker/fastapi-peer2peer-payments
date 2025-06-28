from typing import Optional
from pydantic import BaseModel
from dotenv import dotenv_values
from secrets import token_hex
import os
import logging

logger= logging.getLogger(__name__)

class Config(BaseModel):
    db_host:Optional[str]="localhost"
    db_port:Optional[str]="5432"
    db_user:Optional[str]="peertopeer"
    db_password:Optional[str]="peertopeer"
    db_name:Optional[str]="peertopeer"
    db_pool_size:Optional[int]=10
    db_max_overflow:Optional[int]=20
    token_secret:Optional[str]=token_hex(32)
    admin_username:Optional[str]="audit_admin"
    admin_email:Optional[str]="audit_admin@peertopeer.io"
    admin_password:Optional[str]="tKWaBl50987e"
    admin_first_name:Optional[str]="Audit"
    admin_last_name:Optional[str]="Admin"
    processing_fees:Optional[float]=0.01
env_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")
logger.info(f"### Loading environment variables from {env_path} ......")
config_env=dotenv_values(env_path)

config=Config(**config_env)