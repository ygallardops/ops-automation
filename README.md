# Ops Automation Suite

![CI Status](https://github.com/ygallardops/ops-automation/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green)

Biblioteca centralizada de automatización para mantenimiento operativo en Cloud (AWS/Azure) y On-Premise. Diseñada con principios de ingeniería de Software: modularidad, idempotencia y testing automatizado.

## Características

- **Arquitectura modular:** Separación clara entre lógica de negocio (`src/ops_core`) y scripts de ejecución (`scripts/`).
- **Cloud design:** Módulos extensibles para AWS y Azure.
- **Calidad de código:** Pipeline de CI/CD con GitHub Actions (Linting, Formatting, Unit Testing).
- **Documentación:** Generación automática de docs técnicos con MkDocs.
- **Logging:** Trazabilidad completa de ejecuciones.

## Estructura del proyecto

```text
ops-automation/
├── .github/workflows/      # Pipelines de CI/CD (GitHub Actions)
├── config/
│   └── rules.yaml          # Configuración centralizada (Retención, Endpoints)
├── docs/                   # Documentación técnica (MkDocs)
├── scripts/                # Interfaz de Ejecución (CLI)
│   ├── aws-clean.sh        # Wrapper para limpieza de AWS
│   ├── monitor.sh          # Wrapper para monitoreo de salud
│   └── ...                 # Scripts internos de Python
├── src/
│   └── ops_core/           # Lógica de Negocio (Paquete Python)
│       ├── aws/            # Gestión de recursos AWS
│       ├── azure/          # Gestión de recursos Azure
│       ├── common/         # Utilidades transversales (Logging, Config)
│       └── health/         # Motor de verificaciones HTTP
├── tests/                  # Tests Unitarios con Mocks (Pytest)
├── .flake8                 # Configuración de Linter
├── .pre-commit-config.yaml # Hooks de calidad de código
├── Makefile                # Comandos de automatización de tareas
└── pyproject.toml          # Gestión de dependencias moderna
```
## Quick Start

### Prerrequisitos

-   Python 3.9+: Lenguaje base.
-   Shell Unix/Linux:
    -   Linux/macOS: Terminal estándar.
    - Windows: Se requiere Git Bash (recomendado) o WSL para ejecutar los scripts de la carpeta scripts/.
-   Make (Opcional): Para ejecutar comandos abreviados como make test o make run-aws.
-   AWS CLI (Opcional): Solo necesario si se desea ejecutar la limpieza contra una cuenta real (no requerido para tests unitarios).

### Instalación

Clonar el repositorio:

``` bash
git clone https://github.com/ygallardops/ops-automation.git
cd ops-automation
```

Configurar entorno:

``` bash
# Opcion recomendada usando Make
make setup

# O manual:
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

Ejecutar Tests:

``` bash
make test
```
## Documentación

``` bash
mkdocs serve
```

Luego abre http://127.0.0.1:8000 en tu navegador.

## Contribución

``` bash
make format
make lint
```

## Licencia

MIT License
