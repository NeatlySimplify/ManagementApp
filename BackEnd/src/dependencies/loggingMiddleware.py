import logging
import traceback

from fastapi.exceptions import HTTPException, RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("fastapi.middleware")

class ErrorLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request.state.body = await request.body()

        try:
            response = await call_next(request)
            # Optional: log all responses with non-2xx status
            if response.status_code >= 400:
                logger.warning(
                    "Non-2xx response: %s %s -> %s",
                    request.method,
                    request.url,
                    response.status_code
                )
            return response

        except HTTPException as http_exc:
            logger.exception(
                "HTTPException: %s %s\nStatus: %s\nDetail: %s",
                request.method,
                request.url,
                http_exc.status_code,
                http_exc.detail
            )
            raise  # Let FastAPI handle it

        except RequestValidationError as val_err:
            body = await request.body()
            logger.warning(
                "ValidationError: %s %s\nBody: %s\nErrors: %s",
                request.method,
                request.url,
                body.decode("utf-8"),
                val_err.errors()
            )
            raise  # Let FastAPI return the 422

        except Exception:
            body = await request.body()
            logger.critical(
                "Unhandled Exception: %s %s\nBody: %s\nTraceback:\n%s",
                request.method,
                request.url,
                body.decode("utf-8"),
                traceback.format_exc()
            )
            # Optionally return a safe response (or let global handler take over)
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error"},
            )
