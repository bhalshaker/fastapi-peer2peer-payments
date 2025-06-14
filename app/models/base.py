import uuid
from sqlalchemy.orm import declarative_base 
from sqlalchemy import Column, DateTime, func,UUID

Base = declarative_base()

class BaseModel(Base):
    """
    BaseModel is an abstract base class for all database models in the application.
    Attributes:
        id (UUID): The primary key for the model, automatically generated as a UUID.
        created_at (DateTime): The timestamp when the record was created, defaults to the current time.
        modified_at (DateTime): The timestamp when the record was last modified, automatically updated on changes.
    """
    __abstract__ = True
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
