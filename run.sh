#!/usr/bin/env bash
set -e

# Simple one-command runner for gpu-tpu-roi
# Usage: bash run.sh

if [ -d ".venv" ]; then
  echo "Using existing .venv"
else
  echo "Creating virtualenv in .venv"
  python3 -m venv .venv
fi

# shellcheck disable=SC1091
source .venv/bin/activate

pip install --upgrade pip >/dev/null
pip install -r requirements.txt

echo "Starting FastAPI app at http://localhost:8000/ ..."
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
