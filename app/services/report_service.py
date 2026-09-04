from uuid import UUID

from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.repositories.report_repository import ReportRepository
from app.schemas.report import ReportCreate


class ReportService:
    def __init__(self, db: Session):
        self.repo = ReportRepository(db)

    def create(self, payload: ReportCreate):
        return self.repo.create(payload)

    def get(self, report_id: UUID):
        obj = self.repo.get(report_id)

        if obj is None:
            raise HTTPException(
                status_code=404,
                detail="Report not found",
            )

        return obj

    def list(self, offset: int, limit: int):
        return self.repo.list(
            offset=offset,
            limit=limit,
        )