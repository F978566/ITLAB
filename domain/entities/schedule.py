from dataclasses import dataclass
from datetime import datetime
from typing import List

from domain.entities.base import BaseEntity
from domain.entities.subject import SubjectEntity
from domain.values.week_kind import WeekKindEnum


@dataclass
class ScheduleEntity(BaseEntity):
    week: WeekKindEnum
    subjects: List[SubjectEntity]