from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.ml.model_loader import artifacts_ready

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
def health(db: Session = Depends(get_db)) -> dict[str, str | bool]:
    database = "disconnected"
    try:
        db.execute(text("SELECT 1"))
        database = "connected"
    except Exception:
        database = "disconnected"
    return {
        "status": "ok" if database == "connected" else "degraded",
        "database": database,
        "model_loaded": artifacts_ready(),
    }
