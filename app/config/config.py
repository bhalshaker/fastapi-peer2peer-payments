from pydantic import BaseModel
from dotenv import dotenv_values

class Config(BaseModel):
    db_host:str
    db_port:str
    db_user:str
    db_password:str
    db_name:str
    db_pool_size:int=10
    db_max_overflow:int=20
    token_secret:str
    admin_username:str="audit_admin"
    admin_email:str="audit_admin@peertopeer.io"
    admin_password:str="tKWaBl50987e"
    admin_first_name:str="Audit"
    admin_last_name:str="Admin"

config_env=dotenv_values(".env")

config=Config(**config_env)