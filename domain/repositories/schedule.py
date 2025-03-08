from typing import Protocol

from domain.entities.week_schedule import WeekScheduleEntity


class ScheduleRepository(Protocol):
    def get_schedule(self) -> tuple[WeekScheduleEntity, WeekScheduleEntity]: ...
