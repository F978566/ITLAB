from abc import ABC
from uuid import uuid4

from pydantic import BaseModel, Field


class BaseEntity(BaseModel, ABC):
    oid: str = Field(default_factory=lambda: str(uuid4()))

    class Config:
        arbitrary_types_allowed = True