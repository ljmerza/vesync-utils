# VeSync Filter Reset API

A simple FastAPI service that resets filters on all VeSync fans.

## Setup

1. Copy the example environment file and add your credentials:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` with your VeSync account details:
   ```
   VESYNC_EMAIL=your_email@example.com
   VESYNC_PASSWORD=your_password
   VESYNC_TIMEZONE=America/New_York
   ```

## Running with Docker

```bash
docker compose up --build -d
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Reset All Fan Filters
```bash
curl -X POST http://localhost:8000/reset-filters
```

Response:
```json
{
  "status": "success",
  "results": [
    {"device": "Living Room Fan", "reset": true},
    {"device": "Bedroom Fan", "reset": true}
  ]
}
```

## Running Locally (without Docker)

```bash
pip install -r requirements.txt
uvicorn app:app --host 0.0.0.0 --port 8000
```
