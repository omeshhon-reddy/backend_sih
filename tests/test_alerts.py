from unittest.mock import patch

from tests.conftest import CRITICAL_FEATURES, REPORT_BODY, fake_critical_result


def test_critical_prediction_creates_alert(client):
    created = client.post("/api/reports", json=REPORT_BODY).json()
    with patch("app.services.report_service.predictor.predict", side_effect=fake_critical_result):
        client.post(f"/api/risk/predict/{created['id']}", json={"features": CRITICAL_FEATURES})
    alerts = client.get("/api/alerts")
    assert alerts.status_code == 200
    assert len(alerts.json()) == 1
    assert alerts.json()[0]["alert_type"] == "risk_alert"


def test_websocket_connect_and_broadcast(client):
    created = client.post("/api/reports", json=REPORT_BODY).json()
    with client.websocket_connect("/ws/alerts") as websocket:
        with patch("app.services.report_service.predictor.predict", side_effect=fake_critical_result):
            client.post(f"/api/risk/predict/{created['id']}", json={"features": CRITICAL_FEATURES})
        event = websocket.receive_json()
        assert event["event"] == "risk_alert"
        assert event["risk_tier"] == "CRITICAL"
        assert event["report_id"] == created["id"]
