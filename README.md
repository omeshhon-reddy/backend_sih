# LandGuard Backend

Central FastAPI hub for **LandGuard**: field reports, PostgreSQL, Phase 3 LightGBM landslide risk inference, GIS map points, and WebSocket alerts.

The deployed dashboard at [https://landguard-eight.vercel.app/](https://landguard-eight.vercel.app/) currently presents a demo operations UI. This backend keeps the documented report JSON contract and exposes GIS/risk/alert APIs the map layer can call.

## Pipeline

```text
Frontend JSON → FastAPI / Pydantic → PostgreSQL
                              ↓
                    Feature service (12 leakage-safe fields)
                              ↓
                    LightGBM adapter (preprocessor.pkl + model.pkl)
                              ↓
                    Risk + optional CRITICAL alert → WebSocket /ws/alerts
```

Latitude/longitude are **GIS metadata only**. They are never sent into the model (Phase 3 leakage rules).

## Requirements

- Python 3.10+
- PostgreSQL 16 (or Docker)
- The two model files from `Desktop/landslide_model`:
  - `preprocessor.pkl`
  - `landslide_xgboost_model.pkl`

## Setup

```powershell
cd "$env:USERPROFILE\OneDrive\Desktop\landguard-backend"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Start Postgres:

```powershell
docker compose up -d db
```

Run migrations:

```powershell
alembic upgrade head
```

Copy ML artifacts if they are not already in `ml_artifacts/`:

```powershell
New-Item -ItemType Directory -Force ml_artifacts | Out-Null
Copy-Item "$env:USERPROFILE\OneDrive\Desktop\landslide_model\preprocessor.pkl" ml_artifacts\
Copy-Item "$env:USERPROFILE\OneDrive\Desktop\landslide_model\landslide_xgboost_model.pkl" ml_artifacts\
```

Run the API:

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

- Swagger: http://127.0.0.1:8000/docs
- Health: `GET /api/health`

## External report contract

`POST /api/reports`

```json
{
  "longitude": 92.62,
  "latitude": 27.47,
  "report": "Landslide reported",
  "report_description": "Heavy rainfall caused soil movement"
}
```

Optional nested `features` (exactly the 12 Phase 3 fields) runs inference after the report is stored. Coordinates must not appear inside `features`.

## Main routes

| Method | Path | Purpose |
|--------|------|---------|
| GET | `/api/health` | Process + database + model status |
| POST | `/api/reports` | Create report (optional `features`) |
| GET | `/api/reports` | Paginated list |
| GET | `/api/reports/{id}` | One report + latest risk if present |
| POST | `/api/risk/predict/{id}` | Run/re-run ML (`{"features": {...}}`) |
| GET | `/api/risk/{id}` | Latest prediction |
| GET | `/api/gis/reports` | Map points (all reports) |
| GET | `/api/gis/risk` | Map points that already have risk |
| GET | `/api/alerts` | Stored alerts |
| WS | `/ws/alerts` | Real-time `risk_alert` events |

## Risk tiers (from the trained model)

| Score | Level | Tier | Default alert |
|-------|-------|------|----------------|
| < 0.30 | 0 | LOW | no |
| 0.30–0.60 | 1 | MEDIUM | no |
| 0.60–0.85 | 2 | HIGH | no |
| ≥ 0.85 | 3 | CRITICAL | **yes** (`ALERT_MIN_TIER=CRITICAL`) |

If soil moisture is unknown, send `soil_moisture: 0.5348` and `soil_moisture_available: 0`.

## Tests

```powershell
pytest
```

## Frontend notes

The live Vercel app is a SIH demo dashboard (role login, Tawang map, mock telemetry). It does not currently call these REST routes. Wire it to:

- `POST /api/reports` for citizen/officer field reports
- `GET /api/gis/risk` for map markers
- `ws://<host>/ws/alerts` for live CRITICAL alerts

Keep CORS origins in `.env` (`CORS_ORIGINS`).
