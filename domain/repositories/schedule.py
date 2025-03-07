from typing import Protocol

from domain.entities.schedule import ScheduleEntity


class ScheduleRepository(Protocol):
    def get_schedule(self) -> tuple[ScheduleEntity, ScheduleEntity]: ...
