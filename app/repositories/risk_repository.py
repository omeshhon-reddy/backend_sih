from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.risk_prediction import RiskPrediction


class RiskRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, prediction: RiskPrediction) -> RiskPrediction:
        self.db.add(prediction)
        self.db.commit()
        self.db.refresh(prediction)
        return prediction

    def latest_for_report(self, report_id: UUID) -> RiskPrediction | None:
        return self.db.scalar(
            select(RiskPrediction)
            .where(RiskPrediction.report_id == report_id)
            .order_by(RiskPrediction.created_at.desc())
            .limit(1)
        )

    def list_for_report(self, report_id: UUID) -> list[RiskPrediction]:
        return list(
            self.db.scalars(
                select(RiskPrediction)
                .where(RiskPrediction.report_id == report_id)
                .order_by(RiskPrediction.created_at.desc())
            )
        )
