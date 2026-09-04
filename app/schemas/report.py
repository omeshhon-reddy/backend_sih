from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class ReportCreate(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True
    )

    longitude: float = Field(ge=-180, le=180)
    latitude: float = Field(ge=-90, le=90)
    report: str = Field(min_length=1, max_length=255)
    report_description: str = Field(min_length=1, max_length=5000)


class ReportResponse(ReportCreate):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    updated_at: datetime