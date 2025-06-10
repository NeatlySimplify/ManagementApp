from functools import wraps

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder


def handle_result():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            result = await func(*args, **kwargs)
            if result is None:
                raise HTTPException(status_code=404, detail="Not existent")
            return {'status': 'success', 'result': jsonable_encoder(result)}
        return wrapper
    return decorator
