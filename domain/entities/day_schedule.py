from typing import List

from domain.entities.base import BaseEntity
from domain.entities.subject import SubjectEntity
from domain.values.day import DayEnum


class DayScheduleEntity(BaseEntity):
    day_of_week: DayEnum
    subjects: List[SubjectEntity]