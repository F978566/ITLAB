from typing import Protocol
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.title import TitleEntity


class TitleRepository(Protocol):
    def check_title_exist(self, title: str, db: AsyncSession) -> bool: ...

    def get_title_by_name(self, title: str, db: AsyncSession) -> TitleEntity: ...