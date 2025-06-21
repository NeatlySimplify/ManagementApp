import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic.networks import EmailStr


class EntityUpdate(BaseModel):
    id: UUID
    email: EmailStr | None = None
    type_tag: str | None = None
    document_type: str | None = None
    status: bool | None = None
    document: str | None = None
    name: str | None = None
    sex: str | None = None
    relationship_status: str | None = None
    notes: dict[str, str | int | float] | None = None
    birth: datetime.date | None = None


class EntityCreate(BaseModel):
    email: str
    type_tag: str
    document_type: str
    status: bool | None = False
    document: str
    name: str
    sex: str | None = None
    relationship_status: str | None = None
    birth: datetime.date | None = None
    notes: dict[str, str | int | float] | None = None


class AddressUpdate(BaseModel):
    id: UUID
    state: str | None = None
    city: str | None = None
    district: str | None = None
    street: str | None = None
    number: int | None = None
    complement: str | None = None
    postal: str | None = None


class AddressCreate(BaseModel):
    entity: UUID
    state: str
    city: str
    district: str
    street: str
    number: int | None = None
    complement: str | None = None
    postal: str | None= None


class ContactUpdate(BaseModel):
    entity: UUID
    number: str | None = None
    type_tag: str | None = None
    extra_email: EmailStr | None = None
    notes: dict[str, str | int | float] | None = None


class ContactCreate(BaseModel):
    entity: UUID
    number: str
    type_tag: str
    extra_email: EmailStr | None
    notes: dict[str, str | int | float] | None = None
