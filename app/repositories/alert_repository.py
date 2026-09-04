from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.alert import Alert


class AlertRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, alert: Alert) -> Alert:
        self.db.add(alert)
        self.db.commit()
        self.db.refresh(alert)
        return alert

    def get(self, alert_id: UUID) -> Alert | None:
        return self.db.scalar(
            select(Alert).where(Alert.id == alert_id)
        )

    def list_recent(
        self,
        *,
        limit: int = 50,
    ) -> list[Alert]:
        return list(
            self.db.scalars(
                select(Alert)
                .order_by(Alert.created_at.desc())
                .limit(limit)
            )
        )

    def list(
        self,
        offset: int = 0,
        limit: int = 100,
        status: str | None = None,
    ) -> list[Alert]:
        query = (
            select(Alert)
            .order_by(Alert.created_at.desc())
            .offset(offset)
            .limit(limit)
        )

        if status:
            query = query.where(Alert.status == status)

        return list(self.db.scalars(query).all())