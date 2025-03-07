from domain.repositories.schedule import ScheduleRepository


class ScheduleService:
    def __init__(self, schedule_repository: ScheduleRepository):
        self.schedule_repository = schedule_repository
        
    def find_problems(self):
        ...