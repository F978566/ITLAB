from typing import Dict, List
from fastapi import APIRouter, Depends
from pydantic import BaseModel

from application.services.schedule import ScheduleProblemsService
from domain.entities.problem_list import ProblemListEntity
from domain.repositories.schedule import ScheduleRepository
from infrastructure.di import create_container
from infrastructure.repositories.schedule import ScheduleRepositoryImpl
from infrastructure.services.schedule import ScheduleServiceImpl


router = APIRouter(
    tags=["problems"],
    prefix="/problems",
)


def get_problems_service() -> ScheduleProblemsService:
    container = create_container()
    return container.resolve(ScheduleProblemsService)


@router.get("/{title}", response_model=Dict[str, ProblemListEntity])
async def get_problem(
    title: str | None = None,
    schedule_problems_service: ScheduleProblemsService = Depends(get_problems_service),
):
    schedule_problems_service.find_problems(title)
    return schedule_problems_service.problems


@router.get("/", response_model=Dict[str, ProblemListEntity])
async def get_default_problem(
    schedule_problems_service: ScheduleProblemsService = Depends(get_problems_service),
):
    schedule_problems_service.find_problems("")
    return schedule_problems_service.problems
