from uuid import UUID
from pydantic import BaseModel
from decimal import Decimal
import datetime


class ModelID(BaseModel):
    id: UUID


class EntityResume(ModelID):
    name: str


class SchedulerResume(ModelID):
    name: str
    type: str
    status: bool
    date: datetime.date


class MovementResume(ModelID):
    type: str
    value: Decimal
    instalment: int


class RecordCreate(BaseModel):
    name: str
    id_service: str | None = None
    active: bool
    status: str | None = None
    type: str
    value: Decimal
    details: dict | None = None
    entity: UUID


class RecordUpdate(ModelID):
    name: str | None = None
    id_service: str | None = None
    active: bool | None = None
    status: str | None = None
    type: str | None = None
    value: Decimal | None = None
    details: dict | None = None


class RecordOut(BaseModel):
    name: str
    id_Service: str
    active: bool
    status: str
    type: str
    details: dict
    value: Decimal
    entity: list[EntityResume]
    event: list[SchedulerResume]
    movement: list[MovementResume]
