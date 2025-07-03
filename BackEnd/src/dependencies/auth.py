from fastapi import Request, HTTPException

async def get_current_user(request: Request):
    token = request.cookies.get("gel-auth-token")
    if not token:
        raise HTTPException(status_code=401)
    return token
