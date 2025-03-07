from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.day import DayEnum


@dataclass
class SubjectEntity(BaseEntity):
    name: str
    time_start: datetime
    time_end: datetime
    location: str
    # day: DayEnum
    day: int