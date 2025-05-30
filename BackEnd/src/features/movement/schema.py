from decimal import Decimal
from pydantic import BaseModel, model_validator
import datetime
from uuid import UUID


class ModelID(BaseModel):
    id: UUID


class PaymentResume(ModelID):
    name: str
    status: bool
    value: Decimal
    payment_date: datetime.date
    is_due: datetime.date


class BankAccountResume(ModelID):
    account_name: str


class RecordResume(ModelID):
    name: str
    id_service: str


class SchedulerResume(ModelID):
    date: datetime.date


class MovementOut(BaseModel):
    type: str
    value: Decimal
    installment: int
    details: dict | None
    record: RecordResume
    account: BankAccountResume
    payment: list[PaymentResume]


class PaymentOut(BaseModel):
    name: str
    type: str
    value: Decimal
    ignore_in_totals: bool
    interest: float | None
    penalty: Decimal | None
    category: str
    subcategory: str | None
    payment_date: datetime.date
    is_due: datetime.date
    status: bool
    movement: ModelID
    event: SchedulerResume

    @model_validator(mode="after")
    def aplicar_juros_e_multa(self) -> "PaymentOut":
        hoje = datetime.date.today()

        if not self.status and self.is_due < hoje:
            # Meses de atraso
            meses_atraso = (hoje.year - self.is_due.year) * 12 + (hoje.month - self.is_due.month)
            meses_atraso = max(meses_atraso, 0)

            juros = Decimal("0.00")
            multa = Decimal("0.00")

            if self.interest:
                juros = self.value * Decimal(self.interest) * meses_atraso
                self.value += juros

            if self.penalty:
                multa = self.penalty
                self.value += multa

        return self



class MovementCreate(BaseModel):
    type: str
    details: dict | None = None
    record: UUID | None = None



class PaymentCreate(BaseModel):
    name: str
    parts: int = 1
    ignore_in_totals: bool = False
    total: Decimal
    payment_date: datetime.date | None = None
    is_due: datetime.date
    status: bool = False
    cycle: str = "Unico"
    bank_account: UUID
    unique: int | None = None
    interest: float | None = None
    penalty: Decimal | None = None
    category: str
    subcategory: str | None


class MovementUpdate(BaseModel):
    id: UUID
    details: dict | None = None


class PaymentUpdate(ModelID):
    name: str | None = None
    value: Decimal | None = None
    interest: float | None = None
    penalty: Decimal | None = None
    ignore_in_totals: bool | None = None
    category: str | None = None
    subcategory: str | None = None
    payment_date: datetime.date | None = None
    is_due: datetime.date | None = None
    status: bool | None = None
    account: UUID | None = None
