from datetime import time
from pydantic import BaseModel


class SubjectEntity(BaseModel):
    name: str
    time_start: time
    time_end: time
    location: str
    day: int
