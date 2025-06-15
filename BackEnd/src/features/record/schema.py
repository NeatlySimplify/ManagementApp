from uuid import UUID
from pydantic import BaseModel


class RecordCreate(BaseModel):
    name: str
    id_service: str | None = None
    active: bool
    status: str | None = None
    type_record: str
    value: str
    notes: dict[str, str | int | float] | None = None
    entity: UUID


class RecordUpdate(BaseModel):
    id: UUID
    name: str | None = None
    id_service: str | None = None
    active: bool | None = None
    status: str | None = None
    type_record: str | None = None
    value: str | None = None
    notes: dict[str, str | int | float] | None = None
