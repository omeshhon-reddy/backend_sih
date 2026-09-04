from __future__ import annotations

import logging
from pathlib import Path
from threading import Lock

import joblib

from app.core.config import settings

logger = logging.getLogger(__name__)

_lock = Lock()
_preprocessor = None
_model = None
_loaded = False


def load_artifacts() -> None:
    global _preprocessor, _model, _loaded
    preprocessor_path = Path(settings.ml_preprocessor_path)
    model_path = Path(settings.ml_model_path)
    if not preprocessor_path.exists() or not model_path.exists():
        logger.warning(
            "ML artifacts not found (preprocessor=%s model=%s); inference will return 503",
            preprocessor_path,
            model_path,
        )
        return
    with _lock:
        _preprocessor = joblib.load(preprocessor_path)
        _model = joblib.load(model_path)
        _loaded = True
        logger.info("Loaded preprocessor %s and model %s", type(_preprocessor).__name__, type(_model).__name__)


def artifacts_ready() -> bool:
    return _loaded and _preprocessor is not None and _model is not None


def get_preprocessor():
    return _preprocessor


def get_model():
    return _model
