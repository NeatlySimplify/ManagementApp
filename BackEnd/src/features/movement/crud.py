# ruff: noqa: TRY003
# pyright: reportAssignmentType=false
import datetime
import json
from dataclasses import asdict
from decimal import ROUND_HALF_EVEN, Decimal
from typing import Tuple, cast, reveal_type
from uuid import UUID

from dateutil.relativedelta import relativedelta

from src.queries.schedule.CreateSchedule_async_edgeql import CreateScheduleResult

from src.dependencies import db
from src.queries.movement import (
    CreateMovement_async_edgeql,
    CreatePayment_async_edgeql,
    DeleteMovement_async_edgeql,
    DeletePayment_async_edgeql,
    GetMovement_async_edgeql,
    GetPayment_async_edgeql,
    UpdateMovement_async_edgeql,
    UpdatePayment_async_edgeql,
)

CycleMap = {
    "Diário": relativedelta(days=1),
    "Semanal": relativedelta(weeks=1),
    "Quinzenal": relativedelta(weeks=2),
    "Mensal": relativedelta(months=1),
    "Trimestral": relativedelta(months=3),
    "Semestral": relativedelta(months=6),
    "Anual": relativedelta(years=1),
    "Personalizado": lambda n: relativedelta(days=n),  # handled specially
}

def date_cycle_generator(
    start: datetime.date,
    period: str,
    count: int,
    custom_days: int| None = None
):
    current: datetime.date = start
    if period == "Único":
        yield start
        return
    for _ in range(count):
        yield current
        delta_spec = CycleMap[period]
        if callable(delta_spec):
            if custom_days is None:
                raise ValueError("custom_days must be provided for 'custom' period.")
            delta: relativedelta = delta_spec(custom_days)
        else:
            delta = delta_spec
        current += delta


def dividir_com_erro_no_final(valor: Decimal, parts: int):
    valor = valor.quantize(Decimal('0.01'))
    parte_base = (valor / parts).quantize(Decimal('0.01'), rounding=ROUND_HALF_EVEN)

    partes_lista = [parte_base] * (parts - 1)
    soma_parcial = sum(partes_lista)
    ultima_parte = (valor - soma_parcial).quantize(Decimal('0.01'))

    partes_lista.append(ultima_parte)
    return partes_lista


@db.handle_database_errors
async def _create_payment(
    db,
    movement: UUID,
    account: UUID,
    name: str,
    value: str,
    ignore_in_totals: bool,
    category: str,
    is_due: datetime.date,
    payment_date: datetime.date | None,
    status: bool,
    type_tag:str
) -> None:
    await CreatePayment_async_edgeql.CreatePayment(
        db,
        name=name,
        value=value,
        ignore_in_totals=ignore_in_totals,
        category=category,
        payment_date=payment_date,
        is_due=is_due,
        status=status,
        account=account,
        movement=movement,
        type_tag=type_tag
    )

@db.handle_database_errors
async def updatePayment(
    db,
    payment: UUID,
    account: UUID | None,
    name: str | None,
    value: str | None,
    ignore_in_totals: bool | None,
    category: str | None,
    payment_date: datetime.date | None,
    is_due: datetime.date | None,
    status: bool | None,
) -> dict | None:
    result = await UpdatePayment_async_edgeql.UpdatePayment(
        db,
        payment_id=payment,
        account=account,
        name=name,
        value=value,
        ignore_in_totals=ignore_in_totals,
        category_tag=category,
        paymentDate=payment_date,
        is_due=is_due,
        status=status
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def getPayment(
    db,
    payment_id: UUID,
) -> dict | None:
    result = await GetPayment_async_edgeql.GetPayment(
        db,
        payment=payment_id
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def deletePayment(
    db,
    payment:UUID,
) -> dict | None:
    result = await DeletePayment_async_edgeql.DeletePayment(db, payment_id=payment)
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def createMovement(
    db,
    type_tag: str,
    details: dict[str, str | int | float] | None,
    record: UUID | None,
    parts: int,
    total: str,
    cycle: str,
    unique: int | None,
    bank_account: UUID,
    name: str,
    ignore_in_totals: bool,
    category: str,
    payment_date: datetime.date | None,
    is_due: datetime.date,
    status: bool,
) -> dict | None:
    result = await CreateMovement_async_edgeql.CreateMovement(
        db,
        type_tag=type_tag,
        record_id=record,
        notes=json.dumps(details) if details is not None else None,
    )
    if result is not None:
        result = asdict(result)
        movement = result["id"]
        if cycle=="Personalizado":
            unique = None
        offset = date_cycle_generator(is_due, cycle, parts, unique)
        value_list = list(map(str, dividir_com_erro_no_final(Decimal(total),parts)))

        for n, i in enumerate(offset):
            await _create_payment(
                db,
                movement=movement,
                account=bank_account,
                name=name,
                value=value_list[n],
                ignore_in_totals=ignore_in_totals,
                category=category,
                payment_date=payment_date if status else i,
                is_due=i,
                status=status,
                type_tag=type_tag
            )
    return result


@db.handle_database_errors
async def updateMovement(
    db,
    movement_id: UUID,
    details: dict[str, str | int | float] | None
) -> dict | None:
    if details is not None:
        result = await UpdateMovement_async_edgeql.UpdateMovement(
            db,
            movement=movement_id,
            notes=json.dumps(details) if details is not None else None,
        )
        if result is None:
            return None
        return asdict(result)
    return None


@db.handle_database_errors
async def deleteMovement(
    db,
    movement_id: UUID,
) -> dict | None:
    result = await DeleteMovement_async_edgeql.DeleteMovement(
        executor=db,
        movement=movement_id
    )
    if result is not None:
        result = asdict(result)
    return result


@db.handle_database_errors
async def getMovement(
    db,
    movement_id: UUID,
) -> dict | None:
    result = await GetMovement_async_edgeql.GetMovement(
        executor=db,
        movement=movement_id
    )
    if result is None:
        return None
    result_dict = asdict(result)
    if result_dict["notes"] is not None:
        result_dict["notes"] = json.loads(result_dict["notes"])
    return result_dict
