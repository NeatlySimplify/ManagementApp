import datetime
from uuid import UUID

from pydantic import BaseModel

class SchedulerCreate(BaseModel):
    type_entry: str
    name: str
    status: bool | None = False
    date: datetime.date
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    notes: dict[str, str | int | float] | None = None
    origin: UUID | None = None


class SchedulerUpdate(BaseModel):
    id: UUID
    name: str | None = None
    type_entry: str | None = None
    status: bool | None = None
    date: datetime.date | None = None
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    notes: dict[str, str | int | float] | None = None
