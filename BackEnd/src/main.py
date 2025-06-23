import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from src.dependencies.db import lifetime
from src.dependencies.loggingMiddleware import ErrorLoggingMiddleware
from src.features.auth.endpoints import authRoute
from src.features.entity.endpoints import entityRoute
from src.features.movement.endpoints import movementRoute
from src.features.record.endpoints import recordRoute
from src.features.scheduler.endpoints import eventRoute
from src.features.user.endpoints import userRoute
from src.settings import get_settings

logging.basicConfig(
    level=logging.DEBUG,  # or DEBUG for more verbosity
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)

logger = logging.getLogger('app')


cors_config = {
    "allow_origins": ["http://localhost:8000"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

settings = get_settings()

app = FastAPI(lifespan=lifetime)
app.add_middleware(CORSMiddleware, **cors_config)
app.add_middleware(ErrorLoggingMiddleware)
app.include_router(authRoute)
app.include_router(userRoute)
app.include_router(eventRoute)
app.include_router(movementRoute)
app.include_router(entityRoute)
app.include_router(recordRoute)

current = Path(__file__).parent
index_path = Path(current, "static", "index.html")
_cached_index_html: str = ''


def load_index_html():
    global _cached_index_html
    with index_path.open() as f:
        _cached_index_html = f.read()

load_index_html()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    body = await request.body()
    logger.warning(
        "ValidationError: %s %s\nBody: %s\nErrors: %s",
        request.method,
        request.url,
        body.decode("utf-8"),
        exc.errors()
    )
    return JSONResponse(
        status_code=HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors()}),
    )

app.mount('/assets', StaticFiles(directory='src/static/assets/', html=True), name='assets')


@app.get("/{full_path:path}", response_class=HTMLResponse)
async def catch_all(request: Request, full_path: str):
    if full_path.startswith(("api", "assets")) or "." in full_path:
        raise HTTPException(status_code=404)

    backend_url = str(request.base_url).rstrip("/")
    html = _cached_index_html.replace("__API_URL_PLACEHOLDER__", backend_url)
    return HTMLResponse(content=html, status_code=200)
