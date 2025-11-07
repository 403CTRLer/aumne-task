# WhatsApp Appointment Scheduling System

This project implements a WhatsApp-enabled appointment booking platform composed of:

- **FastAPI backend** for scheduling, cancellation, reminders, and WhatsApp/Twilio integration.
- **React dashboard** for manual appointment management.
- **Python SDK** generated from the OpenAPI specification.
- **Automation scripts** to simplify setup, execution, and SDK generation.

## Architecture Overview

- `backend/` — FastAPI application using SQLModel (SQLite by default) and APScheduler for reminder jobs.
- `frontend/` — React (Vite + TypeScript) dashboard for creating, listing, and canceling appointments.
- `sdk/` — OpenAPI-generated Python client (created via scripts) and a sample usage script.
- `scripts/` — Cross-platform PowerShell/Bash scripts for environment setup, runtime orchestration, and SDK generation.

## Prerequisites

- Python 3.11+
- Node.js 18+
- npm
- (Optional) Docker (for SDK generation) and Java 11+ if you prefer running the OpenAPI Generator without Docker.

## 1. Setup

```powershell
cd D:\aumne
./scripts/setup.ps1
```

```bash
cd /path/to/aumne
./scripts/setup.sh
```

Set `GenerateEnvExamples` (PowerShell) or `GENERATE_ENV_EXAMPLES=1` (Bash) if you want the scripts to scaffold `.env` templates automatically.

### Environment Variables

Create `backend/.env` (or use the template) and supply your Twilio credentials:

```
DATABASE_URL=sqlite:///./appointments.db
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=your_auth_token
WHATSAPP_FROM_NUMBER=whatsapp:+1234567890
REMINDER_LEAD_MINUTES=60
REMINDER_CHECK_INTERVAL_MINUTES=5
```

For the frontend, create `frontend/.env.local` if you need to adjust the API base URL:

```
VITE_API_BASE_URL=http://localhost:8000
```

> **Note:** When Twilio credentials are not provided, the backend falls back to a console logger for outbound messages so that local development and testing still work.

## 2. Running the Stack

```powershell
./scripts/run.ps1 -OpenBrowser
```

```bash
./scripts/run.sh
```

- Backend available at `http://localhost:8000` (Swagger UI: `/docs`).
- Frontend dashboard available at `http://localhost:5173`.

### Manual Commands

```powershell
& .\.venv\Scripts\Activate.ps1
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

```bash
source .venv/bin/activate
uvicorn app.main:app --app-dir backend --host 0.0.0.0 --port 8000
```

In another terminal:

```bash
cd frontend
npm run dev
```

## 3. Running Tests

```powershell
& .\.venv\Scripts\Activate.ps1
pytest backend/tests
```

```bash
source .venv/bin/activate
pytest backend/tests
```

Tests cover appointment creation, cancellation, double-booking protection, and WhatsApp notification dispatch (mocked).

## 4. Python SDK

1. Start the backend locally (OpenAPI spec served from `http://localhost:8000/openapi.json`).
2. Run the generator script:

   ```powershell
   ./scripts/generate-sdk.ps1
   ```

   ```bash
   ./scripts/generate-sdk.sh
   ```

3. Install and try the sample script:

   ```bash
   pip install -e sdk/python-client
   python sdk/sample_usage.py
   ```

## 5. WhatsApp Integration Details

- Outbound messages use Twilio's WhatsApp API. Supply credentials via environment variables.
- Reminder job runs every `REMINDER_CHECK_INTERVAL_MINUTES` and sends messages `REMINDER_LEAD_MINUTES` before the appointment time.
- For environments without Twilio credentials, the service logs messages to the console for visibility.

## 6. Additional Notes

- OpenAPI schema is available at `http://localhost:8000/openapi.json` to support external integrations.
- The frontend prevents duplicate cancellation attempts and displays backend error messages when conflicts occur (e.g., double-booking).
- Feel free to extend the architecture with authentication, Google Calendar integration, or bi-directional WhatsApp workflows.

