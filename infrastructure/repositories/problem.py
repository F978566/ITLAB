from uuid import UUID
from sqlalchemy import select
from domain.entities.problem import ProblemEntity
from domain.repositories.problems import ProblemsRepository
from infrastructure.db.models.models import ProblemModel


class ProblemRepositoryImpl(ProblemsRepository):
    async def get_problems(self, title_id: UUID, db):
        stmt = select(ProblemModel).where(ProblemModel.title_id == title_id)
        result = await db.scalars(stmt)
        res = result.all()
        return [ProblemEntity(oid=x.id, name=x.name, description=x.description) for x in res]