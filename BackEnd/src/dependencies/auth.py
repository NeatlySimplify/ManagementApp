# ruff: noqa: TRY300
from http import HTTPStatus
from typing import Any
from uuid import UUID

import jwt
from fastapi import HTTPException, Request

from src.settings import get_settings

setting = get_settings()

def create_token(user_id: Any, role: str, cookie_type: str = "access"):
    user_id = str(user_id)
    if cookie_type == "refresh":
        payload = {
            "sub": str(user_id),
            "role": str(role),
            "exp": setting.jwt_refresh_exp,
            "type": cookie_type
        }
    else:
        payload = {
            "sub": str(user_id),
            "role": str(role),
            "exp": setting.jwt_exp,
            "type": cookie_type
        }
    return jwt.encode(payload, setting.secret, algorithm=setting.algorithm)


def extract_token(request: Request, token_name: str = "access_token"):
    token = request.cookies.get(token_name)
    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"{token_name.replace('_', ' ').upper()} is missing.",
        )
    return token


def decode_token(token: str, expected_type: str = "access") -> dict[str, str]:
    try:
        payload: dict[str, Any] = jwt.decode(token, setting.secret, algorithms=[setting.algorithm])
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid token type: expected {expected_type}.",
            )
        return {"user": payload["sub"], "role": payload["role"]}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token expired.",
        ) from None
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token.",
        ) from None


async def get_current_user(request: Request):
    try:
        token = extract_token(request, "access_token")
        return decode_token(token, expected_type="access")
    except Exception:
        raise HTTPException(status_code=401, detail="Some error on Auth Token!!!") from None
