from typing import List
from uuid import UUID
from sqlalchemy import select
from domain.entities.title import TitleEntity
from domain.repositories.full_title import FullTitleRepository
from infrastructure.db.models.models import FullTitleModel, TitleModel


class FullTitleRepositoryImpl(FullTitleRepository):
    async def get_full_titles(self, title_id, db) -> List[TitleEntity]:
        query = select(FullTitleModel).where(FullTitleModel.title_id == title_id)
        result = await db.scalars(query)
        res = result.all()
        return [TitleEntity(oid=x.id, title=x.full_title) for x in res]