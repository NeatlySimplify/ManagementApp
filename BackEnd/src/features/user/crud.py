from dataclasses import asdict
from uuid import UUID

from fastapi import HTTPException

from src.dependencies import db
import json
from src.dependencies.pwHash import verify_password
from src.queries.user import (
    CreateBankAccount_async_edgeql,
    CreateSettings_async_edgeql,
    DeleteBankAccount_async_edgeql,
    GetBankAccount_async_edgeql,
    GetUserAuth_async_edgeql,
    GetUserData_async_edgeql,
    UpdateBankAccount_async_edgeql,
    UpdateSettings_async_edgeql,
    UpdateUserAuth_async_edgeql,
)


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
        balance: str,
        category: str | None,
        details: dict[str, str | int | float] | None,
        type: str | None,
        ignore: bool,
    ) -> dict | None:

    result = await CreateBankAccount_async_edgeql.CreateBankAccount(
        db,
        user=user,
        bank_name=bank_name,
        account_name=account_name,
        balance=balance,
        category=category,
        ignore_on_totals=ignore,
        type=type,
        notes=json.dumps(details) if details is not None else None,
    )
    if result is not None:
        result = asdict(result)
    return result


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
    if result_dict["notes"] is not None:
        result_dict["notes"] = json.loads(result_dict["notes"])
    return result_dict


@db.handle_database_errors
async def updateBankAccount(
        db,
        bank_account: UUID,
        bank_name: str | None,
        account_name: str | None,
        type: str | None,
        details: dict[str, str | int | float] | None,
        ignore: bool | None,
        category: str | None,
    ) -> dict | None:
    result = await UpdateBankAccount_async_edgeql.UpdateBankAccount(
        db,
        bank_account=bank_account,
        bank_name=bank_name,
        type=type,
        account_name=account_name,
        ignore_on_totals=ignore,
        category=category
    )
    if result is not None:
        result = asdict(result)
    return result



@db.handle_database_errors
async def getData(
        db,
        user: UUID,
    ) -> dict | None:
    result = await GetUserData_async_edgeql.GetUserData(
        db,
        id=user
    )
    if result is not None:
        result = asdict(result)

    return result


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
