from uuid import UUID, uuid4
from fastapi import Request
from src.queries.user import CreateRefreshToken_async_edgeql, GetRefreshToken_async_edgeql, CreateUser_async_edgeql
from src.dependencies.pkce_helpers import decrypt_password, encrypt_password, generate_pkce
import secrets
import httpx
from src.settings import get_settings
from datetime import datetime

setting = get_settings()

GEL_AUTH_BASE_URL = setting.gel_url
PROVIDER = "builtin::local_emailpassword"
REFRESH_EXPIRATION_DAYS = setting.token_expiration

async def register_user(email: str, password: str, name: str, request: Request, db):
    verifier, challenge = generate_pkce()
    server_url = str(request.base_url).rstrip("/")

    url = f"{GEL_AUTH_BASE_URL}/register"
    payload = {
        "email": email,
        "password": password,
        "provider": PROVIDER,
        "challenge": challenge,
        "verify_url": f"{server_url}/auth/verify"
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    response = {"verifier": verifier}
    if "code" in data:
        token = await get_auth_token(data["code"], verifier)
        response["auth_token"] = token

    if "identity_id" in data:
        new_token = uuid4()
        await create_user(new_token, data["identity_id"], name, db)
        response["identity_id"] = data["identity_id"]

    return response

async def login_user(email: str, password: str, db):
    verifier, challenge = generate_pkce()

    url = f"{GEL_AUTH_BASE_URL}/authenticate"
    payload = {
        "email": email,
        "password": password,
        "provider": PROVIDER,
        "challenge": challenge
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    if "code" in data:
        token = await get_auth_token(data["code"], verifier)
        refresh_token = secrets.token_urlsafe(64)
        encrypted_password = encrypt_password(password)
        await store_refresh_token(email, encrypted_password, data["identity_id"], refresh_token, db)
        return {"auth_token": token, "verifier": verifier, "refresh_token": refresh_token}

    return {"auth_token": None, "verifier": verifier, "refresh_token": None}


async def get_auth_token(code: str, verifier: str):
    token_url = f"{GEL_AUTH_BASE_URL}/token"
    params = {"code": code, "verifier": verifier}
    async with httpx.AsyncClient() as client:
        r = await client.get(token_url, params=params)
        r.raise_for_status()
        return r.json()["auth_token"]

async def create_user(refresh_token: UUID, identity_id: UUID, name: str, db):
    await CreateUser_async_edgeql.CreateUser(
        db,
        identity_id=identity_id,
        type_insert="is_individual",
        name=name,
        refreshe_token=refresh_token
    )

async def send_password_reset(email: str, request: Request):
    verifier, challenge = generate_pkce()
    server_url = str(request.base_url).rstrip("/")

    url = f"{GEL_AUTH_BASE_URL}/send-reset-email"
    payload = {
        "email": email,
        "provider": PROVIDER,
        "reset_url": f"{server_url}/reset-password",
        "challenge": challenge
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()

    return {"verifier": verifier, "status": "email_sent"}

async def reset_password(reset_token: str, new_password: str, verifier: str):
    url = f"{GEL_AUTH_BASE_URL}/reset-password"
    payload = {
        "reset_token": reset_token,
        "password": new_password,
        "provider": PROVIDER
    }

    async with httpx.AsyncClient() as client:
        r = await client.post(url, json=payload)
        r.raise_for_status()
        data = r.json()

    token = await get_auth_token(data["code"], verifier)
    return {"auth_token": token}

async def store_refresh_token(
    email: str,
    encrypted_password: str,
    identity_id: UUID,
    token: str,
    db):
    await CreateRefreshToken_async_edgeql.CreateRefreshToken(
        db,
        token=token,
        email=email,
        enc_pw=encrypted_password,
        identity_id=identity_id,
        duration=f"{REFRESH_EXPIRATION_DAYS} days"
    )


async def refresh_auth_token(refresh_token: str, db):
    result = await GetRefreshToken_async_edgeql.GetRefreshToken(db, refresh_token=refresh_token)
    if not result:
        raise ValueError("Invalid or expired refresh token")

    password = decrypt_password(result.encrypted_password)
    login_data = await login_user(result.email, password, db)

    now = datetime.now()
    if (result.expires_at - now).days < 5:
        new_refresh_token = secrets.token_urlsafe(64)
        await store_refresh_token(
            email=result.email,
            encrypted_password=result.encrypted_password,
            identity_id=result.identity.id,
            token=new_refresh_token,
            db=db
        )
        login_data["refresh_token"] = new_refresh_token
    else:
        login_data["refresh_token"] = refresh_token

    return login_data


# @db.handle_database_errors
# async def loginUser(
#     db,
#     email: str,
#     password: str,
# ) -> tuple[dict[str, str | None], bool] | tuple[None, None]:
#     db = db.with_globals({"current_user": admin_id})
#     result: GetUserAuth_async_edgeql.GetUserAuthResult | None = (
#         await GetUserAuth_async_edgeql.GetUserAuth(executor=db, email=email)
#     )

#     if result is None:
#         return None, None
#     result_dict = asdict(result)
#     print(result_dict)
#     return result_dict, verify_password(password, result.password)


# @db.handle_database_errors
# async def createUser(
#     db,
#     email: str,
#     type_insert: str,
#     hash_password: str,
#     name: str,
#     token: UUID,
# ) -> CreateUser_async_edgeql.CreateUserResult | None:
#     db = db.with_globals({"current_user": admin_id})
#     return await CreateUser_async_edgeql.CreateUser(
#         executor=db,
#         name=name,
#         email=email,
#         password=hash_password,
#         refreshe_token=token,
#         type_insert=type_insert
#     )


# @db.handle_database_errors
# async def loginWithToken(
#     db,
#     email: str,
#     token: UUID,
# ) -> tuple[bool, dict] | tuple[None, None]:
#     db = db.with_globals({"current_user": admin_id})
#     result: GetUserAuth_async_edgeql.GetUserAuthResult | None = (
#         await GetUserAuth_async_edgeql.GetUserAuth(
#             executor=db,
#             email=email
#         )
#     )
#     if result is None:
#         return None, None
#     result_dict = asdict(result)
#     return result.refresh_token == token, result_dict


# @db.handle_database_errors
# async def getToken(
#     db,
#     email: str,
# ) -> None | bool:
#     db = db.with_globals({"current_user": admin_id})
#     from src.dependencies.email import email as sender
#     result: GetUserToken_async_edgeql.GetUserTokenResult | None = (
#         await GetUserToken_async_edgeql.GetUserToken(
#             db,
#             email=email
#         )
#     )
#     print(result)
#     if result is None:
#         return None
#     sender.send_email(email, result.refresh_token)
#     return True
