#!/usr/bin/env bash
set -euo pipefail

python=${PYTHON:-python3}

echo "[setup] Creating Python virtual environment"
if [ ! -d ".venv" ]; then
  "$python" -m venv .venv
fi

echo "[setup] Installing Python dependencies"
source .venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
deactivate

if [ "${GENERATE_ENV_EXAMPLES:-0}" = "1" ]; then
  echo "[setup] Writing backend .env template"
  cat <<'EOF' > backend/.env
# Populate with your configuration
DATABASE_URL=sqlite:///./appointments.db
TWILIO_ACCOUNT_SID=
TWILIO_AUTH_TOKEN=
WHATSAPP_FROM_NUMBER=
REMINDER_LEAD_MINUTES=60
REMINDER_CHECK_INTERVAL_MINUTES=5
EOF

  echo "[setup] Writing frontend env template"
  echo "VITE_API_BASE_URL=http://localhost:8000" > frontend/.env.local
fi

echo "[setup] Installing frontend dependencies"
pushd frontend >/dev/null
npm install
popd >/dev/null

echo "[setup] Environment ready"

