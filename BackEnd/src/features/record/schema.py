from uuid import UUID

from pydantic import BaseModel

from src.features.generics.schema import CreateDictType, UpdateDictType


class RecordCreate(BaseModel):
    name: str
    id_service: str | None = None
    active: bool
    status: str | None = None
    type: str
    value: str
    details: list[CreateDictType] | None = None
    entity: UUID


class RecordUpdate(BaseModel):
    id: UUID
    name: str | None = None
    id_service: str | None = None
    active: bool | None = None
    status: str | None = None
    type: str | None = None
    value: str | None = None
    details: UpdateDictType | None = None
