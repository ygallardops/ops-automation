#!/bin/bash

# ==============================================================================
# Ops Automation - AWS Snapshot Cleaner Wrapper
# ==============================================================================
# Descripcion: Prepara el entorno y ejecuta la limpieza de snapshots.
# Uso: ./scripts/aws-clean.sh
# ==============================================================================

# 1. Configuracion de seguridad (Fail Fast)
set -e  # Terminar script si falla un comando
set -u  # Terminar si se usa una variable no declarada
set -o pipefail # Capturar fallos en pipes

# 2. Definicion de rutas relativas (Independiente de donde se ejecute)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VENV_PATH="$PROJECT_ROOT/.venv"
PYTHON_SCRIPT="$PROJECT_ROOT/scripts/run_aws_cleanup.py"

# 3. Validacion del entorno virtual
if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    echo "Please run 'make setup' first."
    exit 1
fi

# 4. Ejecucion
echo "[WRAPPER] Activating environment and starting AWS Cleanup..."

# Usamos una sub-shell explicita para activar el venv
(
    # Detectar SO para la activacion correcta (Windows/Linux)
    if [ -f "$VENV_PATH/Scripts/activate" ]; then
        source "$VENV_PATH/Scripts/activate"
    else
        source "$VENV_PATH/bin/activate"
    fi

    # Configurar PYTHONPATH para incluir 'src'
    export PYTHONPATH="$PROJECT_ROOT/src:${PYTHONPATH:-}"

    # Ejecutar script Python
    python "$PYTHON_SCRIPT"
)

# Capturar el codigo de salida de la sub-shell
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
    echo "[WRAPPER] Execution completed successfully."
else
    echo "[WRAPPER] Execution failed with error code $EXIT_CODE."
fi

exit $EXIT_CODE
