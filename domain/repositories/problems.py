from typing import List, Protocol
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.problem import ProblemEntity


class ProblemsRepository(Protocol):
    def get_problems(self, title_id: UUID, db: AsyncSession) -> List[ProblemEntity]: ...
