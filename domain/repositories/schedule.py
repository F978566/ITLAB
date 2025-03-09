from typing import Protocol

from domain.entities.week_schedule import WeekScheduleEntity


class ScheduleRepository(Protocol):
    def get_schedule_list(self, group: str) -> tuple[WeekScheduleEntity, WeekScheduleEntity]: ...
