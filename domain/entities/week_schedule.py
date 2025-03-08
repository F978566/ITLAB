from typing import List

from domain.entities.base import BaseEntity
from domain.entities.day_schedule import DayScheduleEntity
from domain.values.week_kind import WeekKindEnum


class WeekScheduleEntity(BaseEntity):
    week: WeekKindEnum
    schedule: List[DayScheduleEntity]
    full_group_title: str
