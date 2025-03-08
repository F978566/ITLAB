from domain.entities.week_schedule import WeekScheduleEntity
from domain.repositories.schedule import ScheduleRepository
from domain.services.schedule import ScheduleService


class ScheduleRepositoryImpl(ScheduleRepository):
    def __init__(self, schedule_service: ScheduleService):
        self.schedule_service = schedule_service
    
    def get_schedule_list(self) -> tuple[WeekScheduleEntity, WeekScheduleEntity]:
        return self.schedule_service.get_schedule_list()