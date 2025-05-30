from pydantic import BaseModel
from uuid import UUID
from typing import Optional
import datetime
from pydantic.networks import EmailStr


class ModelID(BaseModel):
    id: UUID

class EntityUpdate(ModelID):
    email: EmailStr | None = None
    type: str | None = None
    id_type: str | None = None
    status: bool | None = None
    govt_id: str | None = None
    name: str | None = None
    sex: str | None = None
    relationship_status: str | None = None
    details: dict | None = None
    birth: datetime.date | None = None


class EntityCreate(ModelID):
    email: str
    type: str
    id_type: str
    status: bool | None = False
    govt_id: str
    name: str
    sex: str | None = None
    relationship_status: str | None = None
    birth: datetime.date | None = None
    details: dict | None = None


class AddressUpdate(ModelID):
    state: str | None = None
    city: str | None = None
    district: str | None = None
    street: str | None = None
    number: int | None = None
    complement: str | None = None
    postal: str | None = None


class AddressCreate(ModelID):
    state: str
    city: str
    district: str
    street: str
    number: int | None = None
    complement: str | None = None
    postal: str | None= None


class ContactUpdate(BaseModel):
    id: UUID
    number: dict | None = None
    name: str | None = None
    email: EmailStr | None = None
    details: dict | None = None


class EntitySimple(ModelID):
    name: str | None


class ContactCreate(BaseModel):
    id: UUID
    number: dict
    name: str
    email: EmailStr | None
    details: dict | None


class EntityOut(EntityCreate):
    phone: list[ContactCreate]
    address: list[AddressCreate]
