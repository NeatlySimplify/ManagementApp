from uuid import UUID
from src.dependencies.pwHash import verify_password
from dataclasses import asdict
from decimal import Decimal
from fastapi import Depends, HTTPException
import json
from src.queries.user import (
    CreateBankAccount_async_edgeql,
    CreateSettings_async_edgeql,
    DeleteBankAccount_async_edgeql,
    GetBankAccount_async_edgeql,
    GetUserData_async_edgeql,
    UpdateSettings_async_edgeql,
    UpdateBankAccount_async_edgeql,
    UpdateUserAuth_async_edgeql,
    GetUserAuth_async_edgeql
)
from src.dependencies import db


@db.handle_database_errors
async def updateUser(
        db,
        user: UUID,
        email: str,
        hash: str,
        old_password: str,
    ) -> UpdateUserAuth_async_edgeql.UpdateUserAuthResult | None:
    result : GetUserAuth_async_edgeql.GetUserAuthResult | None = await GetUserAuth_async_edgeql.GetUserAuth(
        db,
        email=email
    )
    if result is not None and verify_password(old_password, result.password):
        return await UpdateUserAuth_async_edgeql.UpdateUserAuth(
            db,
            password=hash,
            email=email,
            id=user
        )
    raise HTTPException(
        status_code=403,
        detail="Incorrect old password"
    )


@db.handle_database_errors
async def createBankAccount(
        db,
        user: UUID,
        bank_name: str,
        account_name: str,
        balance: Decimal,
        category: str | None,
        details: dict | None,
        type: str | None,
        ignore: bool,
    ) -> CreateBankAccount_async_edgeql.CreateBankAccountResult | None:

    return await CreateBankAccount_async_edgeql.CreateBankAccount(
        db,
        user=user,
        bank_name=bank_name,
        account_name=account_name,
        balance=balance,
        category=category,
        ignore_on_totals=ignore,
        type=type,
        details=json.dumps(details)
    )


@db.handle_database_errors
async def deleteBankAccount(
        db,
        user: UUID,
        bank_id: UUID,
    ) -> DeleteBankAccount_async_edgeql.DeleteBankAccountResult | None:
    return await DeleteBankAccount_async_edgeql.DeleteBankAccount(
        db,
        user=user,
        account=bank_id
    )


@db.handle_database_errors
async def getBankAccount(
        db,
        bank_id:UUID,
    ) -> dict | None:
    result: GetBankAccount_async_edgeql.GetBankAccountResult | None = await GetBankAccount_async_edgeql.GetBankAccount(db, bank_account=bank_id)
    if result is None:
        return None
    result_dict = asdict(result)
    result_dict["details"] = json.loads(result_dict["details"])

    return result_dict


@db.handle_database_errors
async def updateBankAccount(
        db,
        bank_account: UUID,
        bank_name: str | None,
        account_name: str | None,
        type: str | None,
        details: dict | None,
        ignore: bool | None,
        category: str | None,
    ) -> UpdateBankAccount_async_edgeql.UpdateBankAccountResult | None:
    return await UpdateBankAccount_async_edgeql.UpdateBankAccount(
        db,
        bank_account=bank_account,
        bank_name=bank_name,
        type=type,
        account_name=account_name,
        details=json.dumps(details),
        ignore_on_totals=ignore,
        category=category
    )


@db.handle_database_errors
async def getData(
        db,
        user: UUID,
    ) -> GetUserData_async_edgeql.GetUserDataResult | None:
    return await GetUserData_async_edgeql.GetUserData(
        db,
        id=user
    )


@db.handle_database_errors
async def createSettings(
        db,
        record_title: str,
        movement_title: str,
        entity_title: str,
        bank_account: UUID,
        user: UUID,
    ) -> CreateSettings_async_edgeql.CreateSettingsResult | None:
    return await CreateSettings_async_edgeql.CreateSettings(
        db,
        bank_account=bank_account,
        record_title=record_title,
        movement_title=movement_title,
        entity_title=entity_title,
        user=user
    )


@db.handle_database_errors
async def updateSettings(
        db,
        user: UUID,
        bank_account: UUID | None,
        record_title: str | None,
        movement_title: str | None,
        entity_title: str | None,
        account_types: list[str] | None,
        entity_types: list[str] | None,
        entity_id_types: list[str] | None,
        contact_number_types: list[str] | None,
        record_types: list[str] | None,
        record_status: list[str] | None,
        movement_income_types: list[str] | None,
        movement_expense_types: list[str] | None,
        scheduler_types: list[str] | None,
        movement_cycle_types: list[str] | None,
    ) -> UpdateSettings_async_edgeql.UpdateSettingsResult | None:
    return await UpdateSettings_async_edgeql.UpdateSettings(
        db,
        bank_account=bank_account,
        record_title=record_title,
        movement_title=movement_title,
        entity_title=entity_title,
        account_types=account_types,
        entity_types=entity_types,
        entity_id_types=entity_id_types,
        contact_number_types=contact_number_types,
        record_types=record_types,
        record_status=record_status,
        movement_income_types=movement_income_types,
        movement_expense_types=movement_expense_types,
        scheduler_types=scheduler_types,
        movement_cycle_types=movement_cycle_types,
        user=user
    )
