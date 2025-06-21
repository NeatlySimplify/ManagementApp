from dataclasses import asdict
from uuid import UUID

from src.dependencies import db
from src.dependencies.pwHash import verify_password
from src.queries.user import (
    CreateUser_async_edgeql,
    GetUserAuth_async_edgeql,
    GetUserToken_async_edgeql,
)
from src.settings import get_settings

setting = get_settings()
admin_id = setting.admin_id

@db.handle_database_errors
async def loginUser(
    db,
    email: str,
    password: str,
) -> tuple[dict[str, str | None], bool] | tuple[None, None]:
    db = db.with_globals({"current_user": admin_id})
    result: GetUserAuth_async_edgeql.GetUserAuthResult | None = (
        await GetUserAuth_async_edgeql.GetUserAuth(executor=db, email=email)
    )

    if result is None:
        return None, None
    result_dict = asdict(result)
    return result_dict, verify_password(password, result.password)


@db.handle_database_errors
async def createUser(
    db,
    email: str,
    type_insert: str,
    hash_password: str,
    name: str,
    token: UUID,
) -> CreateUser_async_edgeql.CreateUserResult | None:
    db = db.with_globals({"current_user": admin_id})
    return await CreateUser_async_edgeql.CreateUser(
        executor=db,
        name=name,
        email=email,
        password=hash_password,
        refreshe_token=token,
        type_insert=type_insert
    )


@db.handle_database_errors
async def loginWithToken(
    db,
    email: str,
    token: UUID,
) -> tuple[bool, dict] | tuple[None, None]:
    db = db.with_globals({"current_user": admin_id})
    result: GetUserAuth_async_edgeql.GetUserAuthResult | None = (
        await GetUserAuth_async_edgeql.GetUserAuth(
            executor=db,
            email=email
        )
    )
    if result is None:
        return None, None
    result_dict = asdict(result)
    return result.refresh_token == token, result_dict


@db.handle_database_errors
async def getToken(
    db,
    email: str,
) -> None | bool:
    db = db.with_globals({"current_user": admin_id})
    from src.dependencies.email import email as sender
    result: GetUserToken_async_edgeql.GetUserTokenResult | None = (
        await GetUserToken_async_edgeql.GetUserToken(
            db,
            email=email
        )
    )
    if result is None:
        return None
    sender.send_email(email, result.refresh_token)
    return True
