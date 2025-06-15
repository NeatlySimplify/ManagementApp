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
    result = await getData(db, user)
    return result


@userRoute.put('/', response_class=JSONResponse)
@handle_result()
async def updateUserData(data: UserUpdate, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await updateUser(
        db,
        user=user,
        email=data.email,
        hash=data.hash,
        old_password=data.old_password
    )


@userRoute.post('/bank-account', response_class=JSONResponse)
@handle_result()
async def createAccount(data: BankAccountCreate, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await createBankAccount(
        db,
        user=user,
        bank_name=data.bank_name,
        type=data.type_account,
        account_name=data.account_name,
        balance=data.balance,
        category=data.category,
        details=data.notes,
        ignore=data.ignore_on_totals,
    )


@userRoute.delete('/bank-account/{id}', response_class=JSONResponse)
@handle_result()
async def deleteAccount(id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await deleteBankAccount(
        db,
        user=user,
        bank_id=id
    )


@userRoute.get('/bank-account/{id}', response_class=JSONResponse)
@handle_result()
async def getAccount(id: UUID, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await getBankAccount(
        db,
        bank_id=id
    )


@userRoute.put('/bank-account', response_class=JSONResponse)
@handle_result()
async def updateAccount(bank_account: BankAccountUpdate, user = Depends(get_current_user), db=Depends(get_gel_client)):
    return await updateBankAccount(
        db,
        bank_account=bank_account.id,
        type=bank_account.type_account,
        bank_name=bank_account.bank_name,
        account_name=bank_account.account_name,
        details=bank_account.notes,
        ignore=bank_account.ignore_on_totals,
        category=bank_account.category
    )


@userRoute.post('/settings', response_class=JSONResponse)
@handle_result()
async def createConfig(data: SettingsCreate, user=Depends(get_current_user), db=Depends(get_gel_client)):
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
async def updateConfig(data: SettingsUpdate, user=Depends(get_current_user), db=Depends(get_gel_client)):
    return await updateSettings(
        db,
        user=user,
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
        entity_id_types=data.entity_id_types,
        movement_cycle_types=data.movement_cycle_types,

    )
