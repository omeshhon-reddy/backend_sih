from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class RiskFeatures(BaseModel):
    model_config = ConfigDict(extra="forbid")

    elevation_m: float = Field(ge=0)
    slope_degrees: float = Field(ge=0, le=90)
    aspect_degrees: float = Field(ge=0, le=360)

    rainfall_1d_before: float = Field(ge=0)
    rainfall_3d_before: float = Field(ge=0)
    rainfall_7d_before: float = Field(ge=0)
    rainfall_14d_before: float = Field(ge=0)
    rainfall_30d_before: float = Field(ge=0)

    rainfall_7d_max1d: float = Field(ge=0)
    rainfall_3d_over_7d_ratio: float = Field(ge=0)

    soil_moisture: float = Field(ge=0, le=1)
    soil_moisture_available: int = Field(ge=0, le=1)


class RiskPredictionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    report_id: UUID
    risk_score: float
    risk_level: int
    risk_tier: str
    alert_triggered: bool
    alert_message: str
    created_at: datetime


class RiskResult(BaseModel):
    risk_score: float
    risk_level: int
    risk_tier: str
    alert_triggered: bool
    alert_message: str


# Compatibility with the existing API
PredictRequest = RiskFeatures