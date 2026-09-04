from app.ml.risk_mapping import map_risk_level


def test_risk_mapping_thresholds():
    assert map_risk_level(0.1) == (0, "LOW", False)
    assert map_risk_level(0.3) == (1, "MEDIUM", False)
    assert map_risk_level(0.6) == (2, "HIGH", False)
    assert map_risk_level(0.85) == (3, "CRITICAL", True)
