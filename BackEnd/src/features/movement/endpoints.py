from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from src.dependencies.response_decorator import handle_result
from src.features.movement.schema import (
    ModelID,
    MovementUpdate,
    MovementCreate,
    PaymentCreate,
    PaymentUpdate
)
from src.dependencies.auth import get_current_user
from src.features.movement.crud import (
    deletePayment,
    getMovement,
    getPayment,
    deleteMovement,
    updateMovement,
    createMovement,
    updatePayment
)


movementRoute = APIRouter(prefix='/api/movement')


@movementRoute.get('/', response_class=JSONResponse)
@handle_result()
async def get_movement(movement: ModelID, user=Depends(get_current_user)):
    return await getMovement(movement.id)


@movementRoute.delete('/', response_class=JSONResponse)
@handle_result()
async def delete_movement(movement: ModelID, user=Depends(get_current_user)):
    return await deleteMovement(movement.id)


@movementRoute.put('/', response_class=JSONResponse)
@handle_result()
async def update_movement(data: MovementUpdate, user=Depends(get_current_user)):
    return await updateMovement(
        movement_id=data.id,
        details=data.details
    )


@movementRoute.post('/', response_class=JSONResponse)
@handle_result()
async def create_movement(movement: MovementCreate, payment: PaymentCreate, user=Depends(get_current_user)):
    return await createMovement(
        user=user,
        type=movement.type,
        details=movement.details,
        record=movement.record,
        parts=payment.parts,
        total=payment.total,
        cycle=payment.cycle,
        unique=payment.unique,
        bank_account=payment.bank_account,
        name=payment.name,
        interest=payment.interest,
        penalty=payment.penalty,
        ignore_in_totals=payment.ignore_in_totals,
        category=payment.category,
        subcategory=payment.subcategory,
        payment_date=payment.payment_date,
        is_due=payment.is_due,
        status=payment.status
    )


@movementRoute.get('/payment', response_class=JSONResponse)
@handle_result()
async def get_payment(payment: ModelID, user=Depends(get_current_user)):
    return await getPayment(payment.id)


@movementRoute.delete('/payment', response_class=JSONResponse)
@handle_result()
async def delete_payment(payment: ModelID, user=Depends(get_current_user)):
    return await deletePayment(payment.id)


@movementRoute.put('/payment', response_class=JSONResponse)
@handle_result()
async def update_payment(data: PaymentUpdate, user=Depends(get_current_user)):
    return await updatePayment(
        id=data.id,
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
