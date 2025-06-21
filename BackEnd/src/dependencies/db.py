import logging
import traceback
from contextlib import asynccontextmanager
from functools import wraps
from http import HTTPStatus

import gel
from fastapi import HTTPException, Request
from gel import AsyncIOClient

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifetime(app):
    app.state: AsyncIOClient = gel.create_async_client()
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
            logger.warning("QueryError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Query error occurred.",
                    "details": str(e)
                }
            )

        except gel.errors.IntegrityError as e:
            logger.warning("IntegrityError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.CONFLICT,
                detail={
                    "status": "error",
                    "message": "Integrity constraint violated.",
                    "details": str(e)
                }
            )

        except gel.errors.ExecutionError as e:
            logger.warning("ExecutionError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "Execution error occurred during query execution.",
                    "details": str(e)
                }
            )

        except gel.errors.ProtocolError as e:
            logger.warning("ProtocolError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.BAD_REQUEST,
                detail={
                    "status": "error",
                    "message": "Protocol communication error.",
                    "details": str(e)
                }
            )

        except gel.errors.AccessError as e:
            logger.warning("AccessError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.FORBIDDEN,
                detail={
                    "status": "error",
                    "message": "Access denied.",
                    "details": str(e)
                }
            )

        except gel.errors.BackendError as e:
            logger.warning("BackendError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail={
                    "status": "error",
                    "message": "Database backend error.",
                    "details": str(e)
                }
            )

        except gel.errors.AvailabilityError as e:
            logger.warning("AvailabilityError: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.SERVICE_UNAVAILABLE,
                detail={
                    "status": "error",
                    "message": "Database is temporarily unavailable.",
                    "details": str(e)
                }
            )

        except Exception as e:
            logger.warning("Generic Exception: %s\n%s", str(e), traceback.format_exc())
            raise HTTPException(
                status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
                detail={
                    "status": "error",
                    "message": "An unexpected error occurred.",
                    "details": str(e)
                }
            )
    return wrapper
