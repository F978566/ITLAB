from abc import ABC
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class BaseEntity(BaseModel, ABC):
    oid: UUID = Field(default_factory=lambda: str(uuid4()))

    class Config:
        arbitrary_types_allowed = True