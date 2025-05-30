import datetime
from uuid import UUID
from src.dependencies import db
from fastapi import Depends
from pandas.tseries.offsets import DateOffset
import pandas as pd
from decimal import Decimal
from src.queries.movement import (
    CreateMovement_async_edgeql,
    CreatePayment_async_edgeql,
    DeleteMovement_async_edgeql,
    DeletePayment_async_edgeql,
    GetMovement_async_edgeql,
    GetPayment_async_edgeql,
    UpdateMovement_async_edgeql,
    UpdatePayment_async_edgeql
)


@db.handle_database_errors
async def _create_payment(
        movement: UUID,
        user: UUID,
        account: UUID,
        name: str,
        value: Decimal,
        interest: float | None,
        penalty: Decimal | None,
        ignore_in_totals: bool,
        category: str,
        subcategory: str | None,
        is_due: datetime.date,
        payment_date: datetime.date | None,
        status: bool,
        db=Depends(db.get_gel_client)
    ) -> CreatePayment_async_edgeql.CreatePaymentResult | None:
    return await CreatePayment_async_edgeql.CreatePayment(
        db,
        name=name,
        value=value,
        interest=interest,
        penalty=penalty,
        ignore_in_totals=ignore_in_totals,
        category=category,
        subcategory=subcategory,
        payment_date=payment_date,
        is_due=is_due,
        status=status,
        user=user,
        account=account,
        movement=movement
    )


@db.handle_database_errors
async def updatePayment(
        id: UUID,
        account: UUID | None,
        name: str | None,
        value: Decimal | None,
        interest: float | None,
        penalty: Decimal | None,
        ignore_in_totals: bool | None,
        category: str | None,
        subcategory: str | None,
        payment_date: datetime.date | None,
        is_due: datetime.date | None,
        status: bool | None,
        db=Depends(db.get_gel_client)
    ):
    return await UpdatePayment_async_edgeql.UpdatePayment(
        db,
        payment_id=id,
        account=account,
        name=name,
        value=value,
        interest=interest,
        penalty=penalty,
        ignore_in_totals=ignore_in_totals,
        category=category,
        subcategory=subcategory,
        paymentDate=payment_date,
        is_due=is_due,
        status=status
    )
    return


@db.handle_database_errors
async def getPayment(
        payment_id: UUID,
        db=Depends(db.get_gel_client)
    ) -> GetPayment_async_edgeql.GetPaymentResult | None:
    return await GetPayment_async_edgeql.GetPayment(
        db,
        payment=payment_id
    )


@db.handle_database_errors
async def deletePayment(
        payment:UUID,
        db=Depends(db.get_gel_client)
    ) -> DeletePayment_async_edgeql.DeletePaymentResult | None:
    return await DeletePayment_async_edgeql.DeletePayment(db, payment_id=payment)


@db.handle_database_errors
async def createMovement(
        user: UUID,
        type: str,
        details: dict | None,
        record: UUID | None,
        parts: int,
        total: Decimal,
        cycle: str,
        unique: int | None,
        bank_account: UUID,
        name: str,
        interest: float | None,
        penalty: Decimal | None,
        ignore_in_totals: bool,
        category: str,
        subcategory: str | None,
        payment_date: datetime.date | None,
        is_due: datetime.date,
        status: bool,
        db=Depends(db.get_gel_client)
    ) -> CreateMovement_async_edgeql.CreateMovementResult | None:
    result: CreateMovement_async_edgeql.CreateMovementResult = await CreateMovement_async_edgeql.CreateMovement(
        db,
        type=type,
        user=user,
        details=details,
        record_id=record
    )
    var = unique if unique is not None else 0
    cycles: dict[str, DateOffset | datetime.date] = {
        "Diário": DateOffset(day=1),
        "Semanal": DateOffset(day=7),
        "Quinzenal": DateOffset(day=15),
        "Mensal": DateOffset(month=1),
        "Bimestral": DateOffset(month=2),
        "Trimestral": DateOffset(month=3),
        "Semestral": DateOffset(month=6),
        "Anual": DateOffset(year=1),
        "Personalizado": DateOffset(day=var),
        "Unico": is_due
    }

    new_value = total/parts
    offset = cycles.get(cycle)
    base_date = pd.Timestamp(is_due)

    if cycle == "Unico":
        due_dates = [is_due]
    else:
        due_dates = [(base_date + (i * offset)).date() for i in range(parts)]
    for i in due_dates:

        await _create_payment(
            movement=result.id,
            user=user,
            account=bank_account,
            name=name,
            value=new_value,
            interest=interest,
            penalty=penalty,
            ignore_in_totals=ignore_in_totals,
            category=category,
            subcategory=subcategory,
            payment_date=payment_date,
            is_due=is_due,
            status=status
        )
    return result


@db.handle_database_errors
async def updateMovement(
        movement_id: UUID,
        details: dict | None,
        db=Depends(db.get_gel_client)
    ) -> UpdateMovement_async_edgeql.UpdateMovementResult | None:
    return await UpdateMovement_async_edgeql.UpdateMovement(
        db,
        movement=movement_id,
        details=details
    )
    return


@db.handle_database_errors
async def deleteMovement(
        movement_id: UUID,
        db=Depends(db.get_gel_client)
    ) -> DeleteMovement_async_edgeql.DeleteMovementResult | None:
    return await DeleteMovement_async_edgeql.DeleteMovement(
        executor=db,
        movement=movement_id
    )


@db.handle_database_errors
async def getMovement(
        movement_id: UUID,
        db=Depends(db.get_gel_client)
    ) -> GetMovement_async_edgeql.GetMovementResult | None:
    return await GetMovement_async_edgeql.GetMovement(
        executor=db,
        movement=movement_id
    )
