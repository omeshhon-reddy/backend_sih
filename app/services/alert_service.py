from __future__ import annotations

import asyncio
from typing import Any

from app.core.config import settings
from app.ml.features import TIER_ORDER
from app.ml.risk_mapping import PredictionResult
from app.models.alert import Alert
from app.models.report import Report
from app.models.risk_prediction import RiskPrediction
from app.repositories.alert_repository import AlertRepository
from app.schemas.alert import WebsocketAlertEvent
from app.websocket.manager import manager


class AlertService:
    def __init__(self, alerts: AlertRepository) -> None:
        self.alerts = alerts

    def should_alert(self, result: PredictionResult) -> bool:
        configured = TIER_ORDER[settings.alert_min_tier]
        return TIER_ORDER[result.risk_tier] >= configured

    def maybe_create_and_broadcast(
        self,
        report: Report,
        prediction: RiskPrediction,
        result: PredictionResult,
    ) -> Alert | None:
        if not self.should_alert(result):
            return None
        alert = self.alerts.create(
            Alert(
                report_id=report.id,
                risk_prediction_id=prediction.id,
                alert_type="risk_alert",
                message=result.alert_message,
                status="open",
            )
        )
        event = WebsocketAlertEvent(
            report_id=report.id,
            longitude=report.longitude,
            latitude=report.latitude,
            risk_score=result.risk_score,
            risk_level=result.risk_level,
            risk_tier=result.risk_tier,
            message=result.alert_message,
            alert_id=alert.id,
        )
        self._schedule_broadcast(event.model_dump(mode="json"))
        return alert

    def _schedule_broadcast(self, payload: dict[str, Any]) -> None:
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        loop.create_task(manager.broadcast(payload))
