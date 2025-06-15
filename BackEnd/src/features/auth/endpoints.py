from fastapi import APIRouter, Depends, HTTPException, Request, Response
from fastapi.responses import JSONResponse

from src.dependencies.auth import create_token, decode_token, extract_token, get_current_user
from src.dependencies.db import get_gel_client
from src.features.auth.crud import createUser, getToken, loginUser, loginWithToken
from src.features.auth.schema import Email, Login, LoginOnToken, Register

authRoute = APIRouter(
    prefix="/api/auth"
)

@authRoute.post("/login", response_class=JSONResponse)
async def login(
    request: Request,
    login: Login,
    response: Response,
    db=Depends(get_gel_client)
):
    result, comparisson = await loginUser(db, login.email, login.password)
    if result is None or not comparisson:
        raise HTTPException(
            status_code=404,
            detail="User doesn't exist or password doesn't match."
        )

    a_token = create_token(result, "access")
    r_token = create_token(result, "refresh")
    user_data = {
        "name": result["name"],
        "email": result["email"],
        "first_access": result["first_access"]
    }

    response = JSONResponse(content={"status": "success", "response": user_data})
    response.set_cookie("access_token", a_token)
    response.set_cookie("refresh_token", r_token)
    return response


@authRoute.get("/logout", response_class=JSONResponse)
async def logout(
    request: Request,
    user=Depends(get_current_user)
):
    response = JSONResponse(content={"status": "success"})
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@authRoute.post("/register", response_class=JSONResponse)
async def register(
    request: Request,
    register: Register,
    db=Depends(get_gel_client)
):
    await createUser(db, register.email, register.hash, register.name, register.token)
    return {
        "status": "success"
    }


@authRoute.post("/forgot_password", response_class=JSONResponse)
async def forgot_password(
    request: Request,
    data: Email,
    db=Depends(get_gel_client)
):
    result = await getToken(db, data.email)
    if result is None:
        raise HTTPException(
            status_code=401,
            detail=f"There is no user {data.email} registered"
        )
    return {
        "status": "success"
    }


@authRoute.post("/login_token", response_class=JSONResponse)
async def loginOnToken(
    request: Request,
    login: LoginOnToken,
    response: Response,
    db=Depends(get_gel_client)
):
    comparisson, result = await loginWithToken(db, login.email, login.token)
    if result is None or not comparisson:
        raise HTTPException(
            status_code=404,
            detail="User doesn't exist or token doesn't match."
        )
    a_token = create_token(user, "access")
    r_token = create_token(user, "refresh")
    user_data = {
        "name": result["name"],
        "email": result["email"],
        "first_access": result["first_access"]
    }

    response = JSONResponse(content={"status": "success", "response": user_data})
    response.set_cookie("access_token", a_token)
    response.set_cookie("refresh_token", r_token)
    return {
        "status": "success"
    }


@authRoute.get("/refresh", response_class=JSONResponse)
async def refresh_jwt(
    request: Request,
    response: Response
):
    refresh_token = extract_token(request, "refresh_token")
    user_id = decode_token(refresh_token, expected_type="refresh")
    new_access_token = create_token(user_id)
    response.set_cookie("access_token", new_access_token)
    return {
        "status": "success"
    }
