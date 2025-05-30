from contextlib import asynccontextmanager
from functools import wraps
import gel
from fastapi import Request, HTTPException
from http import HTTPStatus


@asynccontextmanager
async def lifetime(app):
    app.state = gel.create_async_client()
    await app.state.ensure_connected()
    try:
        yield
    finally:
        # Shutdown: Close the Gel client
        await app.state.aclose()
        app.state = None


async def get_gel_client(request: Request) -> gel.AsyncIOClient:
    return request.app.state


def handle_database_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)

        except gel.errors.QueryError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Query error occurred.",
                    "details": str(e)
                }
            )

        except gel.errors.IntegrityError as e:
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail={
                    "status": "error",
                    "message": "Integrity constraint violated.",
                    "details": str(e)
                }
            )

        except gel.errors.ExecutionError as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "Execution error occurred during query execution.",
                    "details": str(e)
                }
            )

        except gel.errors.ProtocolError as e:
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Protocol communication error.",
                    "details": str(e)
                }
            )

        except gel.errors.AccessError as e:
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail={
                    "status": "error",
                    "message": "Access denied.",
                    "details": str(e)
                }
            )

        except gel.errors.BackendError as e:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail={
                    "status": "error",
                    "message": "Database backend error.",
                    "details": str(e)
                }
            )

        except gel.errors.AvailabilityError as e:
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail={
                    "status": "error",
                    "message": "Database is temporarily unavailable.",
                    "details": str(e)
                }
            )

        except Exception as e:
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "An unexpected error occurred.",
                    "details": str(e)
                }
            )
    return wrapper
