from typing import Dict
from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from application.services.schedule import ScheduleProblemsService
from domain.entities.problem_list import ProblemListEntity
from infrastructure.db.get_db import get_db
from infrastructure.di import create_container


router = APIRouter(
    tags=["problems"],
    prefix="/problems",
)


def get_problems_service() -> ScheduleProblemsService:
    container = create_container()
    return container.resolve(ScheduleProblemsService, dependencies={str: "My custom message"})


@router.get("/{title}", response_model=Dict[str, ProblemListEntity])
async def get_problem(
    title: str | None = None,
    schedule_problems_service: ScheduleProblemsService = Depends(get_problems_service),
    db: AsyncSession = Depends(get_db),
):
    schedule_problems_service.title = title
    await schedule_problems_service.find_problems(db)
    return schedule_problems_service.problems


@router.get("/", response_model=Dict[str, ProblemListEntity])
async def get_default_problem(
    schedule_problems_service: ScheduleProblemsService = Depends(get_problems_service),
    db: AsyncSession = Depends(get_db)
):
    await schedule_problems_service.find_problems(db)
    return schedule_problems_service.problems
