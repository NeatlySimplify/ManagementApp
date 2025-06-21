from uuid import UUID

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.dependencies.auth import get_current_user
from src.dependencies.db import get_gel_client
from src.dependencies.response_decorator import handle_result
from src.features.user.crud import (
    createBankAccount,
    createSettings,
    deleteBankAccount,
    getBankAccount,
    getData,
    updateBankAccount,
    updateSettings,
    updateUser,
)
from src.features.user.schema import (
    BankAccountCreate,
    BankAccountUpdate,
    SettingsCreate,
    SettingsUpdate,
    UserUpdate,
)

userRoute = APIRouter(prefix='/api/user')


@userRoute.get('/', response_class=JSONResponse)
@handle_result()
async def getUserData(user = Depends(get_current_user), db=Depends(get_gel_client)):
    db = db.with_globals({"current_user": user.get('user')})
    return await getData(db, user.get("role"))


@userRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateUserData(
    data: UserUpdate,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updateUser(
        db,
        email=data.email,
        hash_password=data.hash,
        old_password=data.old_password
    )


@userRoute.post('/bank-account', response_class=JSONResponse)
@handle_result()
async def createAccount(
    data: BankAccountCreate,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await createBankAccount(
        db,
        bank_name=data.bank_name,
        type_tag=data.type_tag,
        account_name=data.account_name,
        balance=data.balance,
        category=data.category_tag,
        details=data.notes,
        ignore=data.ignore_on_totals,
    )


@userRoute.delete('/bank-account/{account}', response_class=JSONResponse)
@handle_result()
async def deleteAccount(
    account: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await deleteBankAccount(
        db,
        user=user,
        bank_id=account
    )


@userRoute.get('/bank-account/{account}', response_class=JSONResponse)
@handle_result()
async def getAccount(
    account: UUID,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await getBankAccount(
        db,
        bank_id=account
    )


@userRoute.put('/bank-account', response_class=JSONResponse)
@handle_result()
async def updateAccount(
    bank_account: BankAccountUpdate,
    user = Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updateBankAccount(
        db,
        bank_account=bank_account.id,
        type_tag=bank_account.type_tag,
        bank_name=bank_account.bank_name,
        account_name=bank_account.account_name,
        details=bank_account.notes,
        ignore=bank_account.ignore_on_totals,
        category=bank_account.category_tag
    )


@userRoute.post('/settings', response_class=JSONResponse)
@handle_result()
async def createConfig(
    data: SettingsCreate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await createSettings(
        db,
        user=user,
        record_title=data.record_title,
        movement_title=data.movement_title,
        entity_title=data.entity_title,
        bank_account=data.default_bank_account,
    )


@userRoute.put('/settings', response_class=JSONResponse)
@handle_result()
async def updateConfig(
    data: SettingsUpdate,
    user=Depends(get_current_user),
    db=Depends(get_gel_client)
):
    db = db.with_globals({"current_user": user.get('user')})
    return await updateSettings(
        db,
        record_title=data.record_title,
        movement_title=data.movement_title,
        entity_title=data.entity_title,
        bank_account=data.id,
        account_types=data.account_types,
        entity_types=data.entity_types,
        contact_number_types=data.contact_number_types,
        record_types=data.record_types,
        record_status=data.record_status,
        movement_income_types=data.movement_income_types,
        movement_expense_types=data.movement_expense_types,
        scheduler_types=data.scheduler_types,
        entity_id_types=data.entity_document_types,
        movement_cycle_types=data.movement_cycle_types,
    )
