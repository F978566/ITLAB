from dataclasses import dataclass
from domain.entities.base import BaseEntity


@dataclass
class TeacherEntity(BaseEntity):
    name: str