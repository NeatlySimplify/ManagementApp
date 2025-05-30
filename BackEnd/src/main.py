from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from src.dependencies.db import lifetime
from fastapi.middleware.cors import CORSMiddleware
from src.settings import instance
from src.features.auth.endpoints import authRoute
from src.features.entity.endpoints import entityRoute
from src.features.movement.endpoints import movementRoute
from src.features.record.endpoints import recordRoute
from src.features.scheduler.endpoints import eventRoute
from src.features.user.endpoints import userRoute


cors_config = {
    "allow_origins": ["http://localhost:8000"],
    "allow_credentials": True,
    "allow_methods": ["*"],
    "allow_headers": ["*"],
}

instance()
app = FastAPI(lifespan=lifetime)
app.add_middleware(CORSMiddleware, **cors_config)
app.include_router(authRoute)
app.include_router(userRoute)
app.include_router(eventRoute)
app.include_router(movementRoute)
app.include_router(entityRoute)
app.include_router(recordRoute)



app.mount('/assets', StaticFiles(directory='src/static/assets/', html=True), name='assets')


@app.get("/{full_path:path}")
async def catch_all(full_path: str):
    print('Hi')
    if full_path.startswith("api"):
        raise HTTPException(status_code=404)
    if full_path.startswith("assets") or "." in full_path:
        raise HTTPException(status_code=404)
    return FileResponse("static/index.html")
