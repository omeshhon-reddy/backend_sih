from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.schemas.alert import GisRiskPoint
from app.services.report_service import to_report_read


class GisService:
    def __init__(self, db: Session) -> None:
        self.reports = ReportRepository(db)

    def reports(self, *, limit: int, offset: int) -> list[GisRiskPoint]:
        rows, _ = self.reports.list(limit=limit, offset=offset)
        points = []
        for row in rows:
            read = to_report_read(row)
            points.append(
                GisRiskPoint(
                    id=read.id,
                    longitude=read.longitude,
                    latitude=read.latitude,
                    report=read.report,
                    report_description=read.report_description,
                    risk_score=read.risk_score,
                    risk_level=read.risk_level,
                    risk_tier=read.risk_tier,
                    timestamp=read.created_at,
                )
            )
        return points

    def risk_points(self, *, limit: int, offset: int) -> list[GisRiskPoint]:
        return [point for point in self.reports(limit=limit, offset=offset) if point.risk_score is not None]
