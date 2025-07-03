# pyright: reportArgumentType=false
from fastapi import APIRouter, Depends, Request, Response
from fastapi.responses import JSONResponse

from src.dependencies.db import get_gel_client
from src.dependencies.auth import get_current_user
from src.features.auth.crud import register_user, login_user, send_password_reset, reset_password, refresh_auth_token

authRoute = APIRouter(
    prefix="/api/auth"
)

@authRoute.post("/signup")
async def signup(
    email: str,
    password: str,
    name: str,
    is_type: str,
    response: Response,
    request: Request,
    db=Depends(get_gel_client)):
    result = await register_user(is_type, email, password, name, request, db)
    if "auth_token" in result:
        response.set_cookie("gel-auth-token", result["auth_token"], httponly=True)
    if "verifier" in result:
        response.set_cookie("gel-pkce-verifier", result["verifier"], httponly=True)
    return {"status": "ok"}

@authRoute.post("/signin")
async def signin(email: str, password: str, is_type:str, response: Response, db=Depends(get_gel_client)):
    result = await login_user(email, password, db)
    if result["auth_token"]:
        response.set_cookie("gel-auth-token", result["auth_token"], httponly=True)
    if result["verifier"]:
        response.set_cookie("gel-pkce-verifier", result["verifier"], httponly=True)
    return {"status": "ok" if result["auth_token"] else "verify_email"}

@authRoute.post("/send-reset")
async def send_reset(email: str, response: Response, request: Request):
    result = await send_password_reset(email, request)
    response.set_cookie("gel-pkce-verifier", result["verifier"], httponly=True)
    return {"status": "email_sent"}

@authRoute.post("/reset")
async def reset(reset_token: str, password: str, request: Request, response: Response):
    verifier = request.cookies.get("gel-pkce-verifier")
    result = await reset_password(reset_token, password, verifier)
    response.set_cookie("gel-auth-token", result["auth_token"], httponly=True)
    return {"status": "password_reset"}


@authRoute.post("/auth/refresh")
async def refresh(request: Request, response: Response, db=Depends(get_gel_client)):
    refresh_token = request.cookies.get("refresh_token")
    result = await refresh_auth_token(refresh_token, db)
    if result["auth_token"]:
        response.set_cookie("gel-auth-token", result["auth_token"], httponly=True)
    if result["refresh_token"] != refresh_token:
        response.set_cookie("refresh_token", result["refresh_token"], httponly=True)
    return {"status": "refreshed" if result["auth_token"] else "failed"}

@authRoute.get("/logout")
async def logout(request: Request, response: Response, user=Depends(get_current_user)):
    response.delete_cookie("gel-pkce-verifier")
    response.delete_cookie("gel-auth-token")
    response.delete_cookie("refresh_token")
    return JSONResponse(content={"status": "logout"})
