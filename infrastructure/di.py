import punq

from application.services.schedule import ScheduleProblemsService
from domain.repositories.full_title import FullTitleRepository
from domain.repositories.problems import ProblemsRepository
from domain.repositories.schedule import ScheduleRepository
from domain.repositories.title import TitleRepository
from domain.services.schedule import ScheduleService
from infrastructure.repositories.full_title import FullTitleRepositoryImpl
from infrastructure.repositories.problem import ProblemRepositoryImpl
from infrastructure.repositories.schedule import ScheduleRepositoryImpl
from infrastructure.repositories.title import TitleRepositoryImpl
from infrastructure.services.schedule import ScheduleServiceImpl


def create_container():
    container = punq.Container()

    container.register(ScheduleService, ScheduleServiceImpl)
    container.register(ScheduleRepository, ScheduleRepositoryImpl)
    container.register(TitleRepository, TitleRepositoryImpl)
    container.register(FullTitleRepository, FullTitleRepositoryImpl)
    container.register(ProblemsRepository, ProblemRepositoryImpl)
    container.register(ScheduleProblemsService)

    return container
