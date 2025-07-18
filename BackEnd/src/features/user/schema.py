# ruff: noqa: TRY003
from typing import Self
from uuid import UUID

from pydantic import BaseModel, EmailStr, computed_field, model_validator



class BankAccountUpdate(BaseModel):
    id: UUID
    bank_name: str | None = None
    account_name: str | None = None
    type_tag: str | None = None
    notes: dict[str, str | int | float] | None = None
    ignore_on_totals: bool | None = None
    category_tag: str | None = None


class BankAccountCreate(BaseModel):
    bank_name: str
    account_name: str
    type_tag: str | None = None
    balance: str
    notes: dict[str, str | int | float] | None = None
    ignore_on_totals: bool = False
    category_tag: str | None = None



class SettingsCreate(BaseModel):
    default_bank_account: UUID
    record_title: str
    movement_title: str
    entity_title: str


class UserUpdate(BaseModel):
    email: EmailStr
    password: str
    comfirm_password:str
    old_password: str


    @model_validator(mode='after')
    def check_passwords_match(self) -> Self:
        if self.password != self.comfirm_password:
            raise ValueError('Passwords do not match')
        return self


class SettingsUpdate(BaseModel):
    id: UUID
    default_bank_account: UUID | None = None
    record_title: str | None = None
    movement_title: str | None = None
    entity_title: str | None = None
    account_types: list[str] | None = None
    entity_types: list[str] | None = None
    entity_document_types: list[str] | None = None
    contact_number_types: list[str] | None = None
    record_types: list[str] | None = None
    record_status: list[str] | None = None
    movement_income_types: list[str] | None = None
    movement_expense_types: list[str] | None = None
    scheduler_types: list[str] | None = None
    movement_cycle_types: list[str] | None = None
