from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    report_id: UUID
    risk_prediction_id: UUID | None
    alert_type: str
    message: str
    status: str
    created_at: datetime


class AlertEvent(BaseModel):
    event: str = "risk_alert"
    report_id: UUID
    risk_score: float
    risk_level: int
    risk_tier: str
    message: str
    alert_id: UUID

# Backward-compatible name used by AlertService
WebsocketAlertEvent = AlertEvent