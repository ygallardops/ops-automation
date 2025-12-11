#!/bin/bash

# ==============================================================================
# Ops Automation - Health Check Monitor Wrapper
# ==============================================================================

set -e
set -u
set -o pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/check_services.py"

if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

echo "[WRAPPER] Starting Health Monitor..."

(
    if [ -f "$VENV_PATH/Scripts/activate" ]; then
        source "$VENV_PATH/Scripts/activate"
    else
        source "$VENV_PATH/bin/activate"
    fi

    export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"

    python "$PYTHON_SCRIPT"
)

exit $?
