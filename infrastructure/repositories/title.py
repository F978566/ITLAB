from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.title import TitleEntity
from domain.repositories.title import TitleRepository
from infrastructure.db.models.models import TitleModel


class TitleRepositoryImpl(TitleRepository):
    # def __init__(self, db: AsyncSession):
    #     self.db = db
    
    async def check_title_exist(self, title: str, db: AsyncSession) -> bool:
        exists_subquery = select(TitleModel).where(TitleModel.title == title).exists()
        return await db.scalar(select(exists_subquery))
    
    async def get_title_by_name(self, title: str, db: AsyncSession) -> TitleEntity:
       query = select(TitleModel).where(TitleModel.title == title)
       
       res = await db.scalar(query)
       if res == None:
           return
       
       return TitleEntity(oid=res.id, title=res.title)