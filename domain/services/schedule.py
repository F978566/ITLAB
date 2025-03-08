from typing import Protocol

from domain.entities.week_schedule import WeekScheduleEntity


class ScheduleService(Protocol):
    def get_schedule_list(self) -> WeekScheduleEntity: ...
