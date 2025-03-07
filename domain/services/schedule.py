from typing import Protocol

from domain.entities.schedule import ScheduleEntity


class ScheduleService(Protocol):
    def get_schedule(self) -> ScheduleEntity: ...
