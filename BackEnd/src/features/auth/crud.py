from uuid import UUID

from src.dependencies import db
from src.dependencies.pwHash import verify_password
from src.queries.user import (
    CreateUser_async_edgeql,
    GetUserAuth_async_edgeql,
    GetUserToken_async_edgeql,
)


@db.handle_database_errors
async def loginUser(
    db,
    email: str,
    password: str,
) -> tuple[UUID, bool] | tuple[None, None]:
    result: GetUserAuth_async_edgeql.GetUserAuthResult | None = await GetUserAuth_async_edgeql.GetUserAuth(executor=db, email=email)
    if result is None:
        return None, None
    return result.id, verify_password(password, result.password)


@db.handle_database_errors
async def createUser(
    db,
    email: str,
    hash: str,
    name: str,
    token: UUID,
) -> CreateUser_async_edgeql.CreateUserResult | None:
    return await CreateUser_async_edgeql.CreateUser(
        executor=db,
        name=name,
        email=email,
        password=hash,
        refreshe_token=token
    )


@db.handle_database_errors
async def loginWithToken(
    db,
    email: str,
    token: UUID,
) -> tuple[bool, bool|None, UUID] | tuple[None, None, None]:
    result: GetUserAuth_async_edgeql.GetUserAuthResult | None = await GetUserAuth_async_edgeql.GetUserAuth(
        executor=db,
        email=email
    )
    if result is None: return None, None, None
    return result.refresh_token == token, result.use_token, result.id


@db.handle_database_errors
async def getToken(
    db,
    email: str,
) -> None | bool:
    from src.dependencies.email import email as sender
    result: GetUserToken_async_edgeql.GetUserTokenResult | None = await GetUserToken_async_edgeql.GetUserToken(
        db,
        email=email
    )
    if result is None: return None
    sender.send_email(email, result.refresh_token)
    return True
