from typing import List, Protocol
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.title import TitleEntity


class FullTitleRepository(Protocol):
    def get_full_titles(self, title_id: UUID, db: AsyncSession) -> List[TitleEntity]: ...
