import datetime
from uuid import UUID

from pydantic import BaseModel


class MovementCreate(BaseModel):
    type_tag: str
    notes: dict[str, str |int | float] | None = None
    record: UUID | None = None
    name: str
    parts: int = 1
    ignore_in_totals: bool = False
    total: str
    payment_date: datetime.date | None = None
    is_due: datetime.date
    status: bool = False
    cycle: str = "Unico"
    bank_account: UUID
    unique: int | None = None
    category_tag: str


class MovementUpdate(BaseModel):
    id: UUID
    notes: dict[str, str | int | float] | None = None


class PaymentUpdate(BaseModel):
    id: UUID
    name: str | None = None
    value: str | None = None
    ignore_in_totals: bool | None = None
    category_tag: str | None = None
    payment_date: datetime.date | None = None
    is_due: datetime.date | None = None
    status: bool | None = None
    account: UUID | None = None
