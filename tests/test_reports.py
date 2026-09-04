from tests.conftest import CRITICAL_FEATURES, REPORT_BODY


def test_create_and_get_report(client):
    created = client.post("/api/reports", json=REPORT_BODY)
    assert created.status_code == 201
    body = created.json()
    assert body["longitude"] == REPORT_BODY["longitude"]
    assert body["report"] == REPORT_BODY["report"]
    assert body["risk_score"] is None

    listed = client.get("/api/reports")
    assert listed.status_code == 200
    assert listed.json()["total"] == 1

    fetched = client.get(f"/api/reports/{body['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == body["id"]


def test_invalid_report_returns_422(client):
    response = client.post("/api/reports", json={"longitude": 999, "latitude": 0, "report": "x", "report_description": "y"})
    assert response.status_code == 422


def test_missing_report_returns_404(client):
    response = client.get("/api/reports/00000000-0000-0000-0000-000000000001")
    assert response.status_code == 404


def test_gis_endpoints(client):
    client.post("/api/reports", json=REPORT_BODY)
    reports = client.get("/api/gis/reports")
    assert reports.status_code == 200
    assert len(reports.json()) == 1
    risk = client.get("/api/gis/risk")
    assert risk.status_code == 200
    assert risk.json() == []


def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert "database" in response.json()
