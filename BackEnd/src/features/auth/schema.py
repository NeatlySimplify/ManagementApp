from pydantic import BaseModel, EmailStr, computed_field, model_validator
from uuid import UUID, uuid4
from typing_extensions import Self

from src.dependencies.pwHash import hash_password


class Email(BaseModel):
    email: EmailStr


class Login(BaseModel):
    email: EmailStr
    password: str


class BankAccount(BaseModel):
    bankName: str
    accountName: str
    balance: float
    details: dict | None = None
    ignore_on_totals: bool = False
    category: str


class LoginOnToken(BaseModel):
    email: EmailStr
    token: UUID


class Register(Login):
    name: str
    confirm_password: str


    @model_validator(mode="after")
    def comfirm(self) -> Self:
        if self.password != self.confirm_password:
            raise ValueError("Password is not coinciding")
        return self


    @computed_field
    @property
    def token(self) -> UUID:
        return uuid4()


    @computed_field
    @property
    def hash(self) -> str:
        return hash_password(self.password)
