from typing import List
from domain.entities.base import BaseEntity
from domain.entities.problem import ProblemEntity


class ProblemListEntity(BaseEntity):
    problems: List[ProblemEntity]
    full_group_title: str