from pydantic import BaseModel
from uuid import UUID
import datetime


class ModelID(BaseModel):
    id: UUID


class ScheduleOut(BaseModel):
    type: str
    name: str
    status: bool | None
    date: datetime.date
    origin: ModelID | None
    beginning_time: datetime.time | None
    ending_time: datetime.time | None
    details: dict | None = None


class SchedulerCreate(BaseModel):
    type: str
    name: str
    status: bool | None = False
    date: datetime.date
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    details: dict | None = None
    origin: UUID | None = None


class SchedulerUpdate(ModelID):
    name: str | None = None
    type: str | None = None
    status: bool | None = None
    date: datetime.date | None = None
    beginning_time: datetime.time | None = None
    ending_time: datetime.time | None = None
    details: dict | None = None
