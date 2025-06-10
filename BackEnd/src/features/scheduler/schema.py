import datetime
from uuid import UUID

from pydantic import BaseModel

from src.features.generics.schema import CreateDictType, UpdateDictType


class SchedulerCreate(BaseModel):
    type: str
    name: str
    status: bool | None = False
    date: datetime.date
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    details: list[CreateDictType] | None = None
    origin: UUID | None = None


class SchedulerUpdate(BaseModel):
    id: UUID
    name: str | None = None
    type: str | None = None
    status: bool | None = None
    date: datetime.date | None = None
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    details: UpdateDictType | None
