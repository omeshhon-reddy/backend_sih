from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.risk import PredictRequest, RiskPredictionResponse
from app.services.risk_service import RiskService


router = APIRouter(
    prefix="/api/risk",
    tags=["risk"],
)


@router.post(
    "/predict/{report_id}",
    response_model=RiskPredictionResponse,
)
async def predict_risk(
    report_id: UUID,
    payload: PredictRequest,
    db: Session = Depends(get_db),
):
    service = RiskService(db)

    try:
        return service.predict(
            report_id=report_id,
            features=payload.model_dump(),
        )

    except ValueError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        )