# pyright: ignore[reportReturnType]
from http import HTTPStatus
from typing import Any
from uuid import UUID

import jwt
from fastapi import HTTPException, Request

from src.settings import get_settings

set = get_settings()

def create_token(user_id: Any, type: str = "access"):
    user_id = UUID(str(user_id))
    if type == "refresh":
        payload = {
            "sub": str(user_id),
            "exp": set.jwt_refresh_exp,
            "type": type
        }
    else:
        payload = {
            "sub": str(user_id),
            "exp": set.jwt_exp,
            "type": type
        }
    return jwt.encode(payload, set.secret, algorithm=set.algorithm)


def extract_token(request: Request, token_name: str = "access_token"):
    token = request.cookies.get(token_name)
    if not token:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail=f"{token_name.replace('_', ' ').upper()} is missing.",
        )
    return token


def decode_token(token: str, expected_type: str = "access") -> UUID:
    try:
        payload: dict[str, Any] = jwt.decode(token, set.secret, algorithms=[set.algorithm])
        if payload.get("type") != expected_type:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail=f"Invalid token type: expected {expected_type}.",
            )
        return UUID(payload.get("sub"))
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Token expired.",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail="Invalid token.",
        )


async def get_current_user(request: Request):
    try:
        token = extract_token(request, "access_token")
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")

        user_id = decode_token(token, expected_type="access")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Some error on Auth Token!!!")
