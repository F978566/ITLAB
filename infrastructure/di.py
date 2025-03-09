import punq

from application.services.schedule import ScheduleProblemsService
from domain.repositories.schedule import ScheduleRepository
from domain.services.schedule import ScheduleService
from infrastructure.repositories.schedule import ScheduleRepositoryImpl
from infrastructure.services.schedule import ScheduleServiceImpl


def create_container():
    container = punq.Container()

    container.register(ScheduleService, ScheduleServiceImpl)
    container.register(ScheduleRepository, ScheduleRepositoryImpl)
    container.register(ScheduleProblemsService)

    return container
