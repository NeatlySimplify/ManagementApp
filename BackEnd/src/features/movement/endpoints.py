from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_gel_client
from src.dependencies.response_decorator import handle_result
from src.features.movement.crud import (
    createMovement,
    deleteMovement,
    deletePayment,
    getMovement,
    getPayment,
    updateMovement,
    updatePayment,
)
from src.features.movement.schema import (
    MovementCreate,
    MovementUpdate,
    PaymentUpdate,
)

movementRoute = APIRouter(prefix='/api/movement')


@movementRoute.get('/{movement}', response_class=JSONResponse)
@handle_result()
async def get_movement(
    movement: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await getMovement(db, movement)


@movementRoute.delete('/{movement}', response_class=JSONResponse)
@handle_result()
async def delete_movement(
    movement: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await deleteMovement(db, movement)


@movementRoute.put('/', response_class=JSONResponse)
@handle_result()
async def update_movement(
    data: MovementUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updateMovement(
        db,
        movement_id=data.id,
        details=data.notes
    )


@movementRoute.post('/', response_class=JSONResponse)
@handle_result()
async def create_movement(
    movement: MovementCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await createMovement(
        db,
        type_tag=movement.type_tag,
        details=movement.notes,
        record=movement.record,
        parts=movement.parts,
        total=movement.total,
        cycle=movement.cycle,
        unique=movement.unique,
        bank_account=movement.bank_account,
        name=movement.name,
        interest=movement.interest,
        penalty=movement.penalty,
        ignore_in_totals=movement.ignore_in_totals,
        category=movement.category,
        subcategory=movement.subcategory,
        payment_date=movement.payment_date,
        is_due=movement.is_due,
        status=movement.status
    )


@movementRoute.get('/payment/{payment}', response_class=JSONResponse)
@handle_result()
async def get_payment(
    payment: UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await getPayment(db, payment)


@movementRoute.delete('/payment/{payment}', response_class=JSONResponse)
@handle_result()
async def delete_payment(
    payment:UUID,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await deletePayment(db, payment)


@movementRoute.put('/payment', response_class=JSONResponse)
@handle_result()
async def update_payment(
    data: PaymentUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updatePayment(
        db,
        payment=data.id,
        account=data.account,
        name=data.name,
        value=data.value,
        interest=data.interest,
        penalty=data.penalty,
        ignore_in_totals=data.ignore_in_totals,
        category=data.category,
        subcategory=data.subcategory,
        payment_date=data.payment_date,
        is_due=data.is_due,
        status=data.status
    )
