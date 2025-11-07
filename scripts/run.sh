#!/usr/bin/env bash
set -euo pipefail

if [ ! -d ".venv" ]; then
  echo "Virtual environment not found. Run scripts/setup.sh first." >&2
  exit 1
fi

echo "[run] Starting FastAPI backend"
tmux new-session -d -s appointment-stack "source .venv/bin/activate && cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000"

echo "[run] Starting React frontend"
tmux split-window -h "cd frontend && npm run dev -- --host"
tmux attach-session -d

