from uuid import UUID

from pydantic import BaseModel


class RecordCreate(BaseModel):
    name: str
    service_id: str | None = None
    status: bool
    optional_status: str | None = None
    type_tag: str
    value: str
    notes: dict[str, str | int | float] | None = None
    entities: list[UUID]


class RecordUpdate(BaseModel):
    id: UUID
    name: str | None = None
    service_id: str | None = None
    status: bool | None = None
    optional_status: str | None = None
    type_tag: str | None = None
    value: str | None = None
    notes: dict[str, str | int | float] | None = None
