import datetime
from uuid import UUID

from pydantic import BaseModel
from pydantic.networks import EmailStr

from src.features.generics.schema import CreateDictType, UpdateDictType


class EntityUpdate(BaseModel):
    id: UUID
    email: EmailStr | None = None
    type: str | None = None
    id_type: str | None = None
    status: bool | None = None
    govt_id: str | None = None
    name: str | None = None
    sex: str | None = None
    relationship_status: str | None = None
    details: UpdateDictType | None = None
    birth: datetime.date | None = None


class EntityCreate(BaseModel):
    email: str
    type: str
    id_type: str
    status: bool | None = False
    govt_id: str
    name: str
    sex: str | None = None
    relationship_status: str | None = None
    birth: datetime.date | None = None
    details: list[CreateDictType] | None = None


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
    id: UUID
    number: UpdateDictType | None = None
    name: str | None = None
    email: EmailStr | None = None
    details: UpdateDictType | None = None


class ContactCreate(BaseModel):
    entity: UUID
    number: list[CreateDictType]
    name: str
    email: EmailStr | None
    details: list[CreateDictType] | None = None
