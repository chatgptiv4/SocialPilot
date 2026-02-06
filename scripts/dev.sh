#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

BACKEND_VENV="$ROOT_DIR/backend/.venv"

if [[ -f "$BACKEND_VENV/bin/activate" ]]; then
  # shellcheck disable=SC1090
  source "$BACKEND_VENV/bin/activate"
else
  echo "Warning: backend virtualenv not found at $BACKEND_VENV."
  echo "Create it with: cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt"
fi

cleanup() {
  if [[ -n "${BACKEND_PID:-}" ]]; then
    kill "$BACKEND_PID" 2>/dev/null || true
  fi
  if [[ -n "${FRONTEND_PID:-}" ]]; then
    kill "$FRONTEND_PID" 2>/dev/null || true
  fi
}
trap cleanup EXIT

cd "$ROOT_DIR/backend"
uvicorn app.main:app --reload &
BACKEND_PID=$!

cd "$ROOT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!

wait "$BACKEND_PID" "$FRONTEND_PID"
