from dataclasses import dataclass
from datetime import datetime

from domain.entities.base import BaseEntity
from domain.values.day import DayEnum
from domain.values.week_kind import WeekKindEnum


@dataclass
class ScheduleEntity(BaseEntity):
    week: WeekKindEnum
    day: DayEnum
    start_time: datetime
    end_time: datetime
    duration: int