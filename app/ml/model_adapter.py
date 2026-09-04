from __future__ import annotations

import pandas as pd

from app.core.exceptions import InferenceError, InferenceUnavailableError
from app.ml.features import ALL_FEATURES
from app.ml.model_loader import artifacts_ready, get_model, get_preprocessor
from app.ml.risk_mapping import PredictionResult, map_risk_level
from app.core.config import settings


class ModelAdapter:
    """Isolates joblib/LightGBM from FastAPI routes and services."""

    def predict(self, features: dict[str, float | int]) -> PredictionResult:
        if not artifacts_ready():
            raise InferenceUnavailableError("ML model is not loaded")
        missing = [name for name in ALL_FEATURES if name not in features]
        if missing:
            raise InferenceError(f"Incomplete feature set: {missing}")
        try:
            frame = pd.DataFrame([{name: features[name] for name in ALL_FEATURES}], columns=ALL_FEATURES)
            processed = get_preprocessor().transform(frame)
            probability = float(get_model().predict_proba(processed)[0, 1])
        except Exception as exc:  # sklearn/lightgbm failures
            raise InferenceError("Risk prediction failed") from exc

        risk_level, risk_tier, model_alert = map_risk_level(probability)
        message = (
            "IMMEDIATE WARNING: CRITICAL landslide risk! Evacuate and alert authorities."
            if model_alert
            else "No immediate alert. Continue monitoring."
        )
        return PredictionResult(
            risk_score=round(probability, 4),
            risk_level=risk_level,
            risk_tier=risk_tier,
            alert_triggered=model_alert,
            alert_message=message,
            model_version=settings.ml_model_version,
        )
