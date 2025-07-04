import datetime
from uuid import UUID

from pydantic import BaseModel


class SchedulerCreate(BaseModel):
    type_tag: str
    name: str
    status: bool | None = False
    date_beginning: datetime.datetime
    ending_time: datetime.datetime | None = None
    notes: dict[str, str | int | float] | None = None


class SchedulerUpdate(BaseModel):
    id: UUID
    name: str | None = None
    type_tag: str | None = None
    status: bool | None = None
    date_beginning: datetime.datetime | None = None
    ending_time: datetime.datetime | None = None
    notes: dict[str, str | int | float] | None = None
