from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api import alerts, gis, health, reports, risk, ws
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import setup_logging
from app.ml.model_loader import load_artifacts


@asynccontextmanager
async def lifespan(_app: FastAPI):
    setup_logging()
    load_artifacts()
    yield


app = FastAPI(
    title="LandGuard Backend",
    description=(
        "Central hub for LandGuard: field reports, PostgreSQL persistence, "
        "Phase 3 LightGBM risk inference, GIS GeoJSON-friendly points, and WebSocket alerts."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.mount(
    "/uploads",
    StaticFiles(directory="uploads"),
    name="uploads",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(health.router)
app.include_router(reports.router)
app.include_router(risk.router)
app.include_router(gis.router)
app.include_router(alerts.router)
app.include_router(ws.router)

