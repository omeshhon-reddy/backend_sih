from dataclasses import dataclass


def map_risk_level(probability: float) -> tuple[int, str, bool]:
    """Must stay in sync with the Phase 3 LightGBM handover service."""
    if probability < 0.30:
        return 0, "LOW", False
    if probability < 0.60:
        return 1, "MEDIUM", False
    if probability < 0.85:
        return 2, "HIGH", False
    return 3, "CRITICAL", True


@dataclass(frozen=True)
class PredictionResult:
    risk_score: float
    risk_level: int
    risk_tier: str
    alert_triggered: bool
    alert_message: str
    model_version: str

    @property
    def risk_label(self) -> str:
        return self.risk_tier
