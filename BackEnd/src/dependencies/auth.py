# pyright: ignore[reportReturnType]
import jwt
from http import HTTPStatus
from fastapi import HTTPException, Request
from datetime import datetime, timedelta
from src.settings import get_settings
from typing import Any
from uuid import UUID



class TestingVar():
    jwt_expire: float = 5
    algorithm: str = "HS256"
    secret: str = "80af3f6203c32405093db6bd7ebdb126474d495690aa0893"


set = TestingVar()

def create_token(user_id: Any, type: str = "access", expire_time: float = set.jwt_expire):
    user_id = UUID(str(user_id))
    expire = datetime.now() + timedelta(minutes=expire_time)
    if type == "refresh":
        expire = datetime.now() + timedelta(minutes=set.jwt_expire * 30)

    payload = {
        "sub": str(user_id),
        "exp": int(expire.timestamp()),
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
        user_id = decode_token(token, expected_type="access")
        return user_id
    except Exception:
        raise HTTPException(status_code=401, detail="Some error on Auth Token!!!")
