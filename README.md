# Ops Automation Suite

![CI Status](https://github.com/ygallardops/ops-automation/actions/workflows/ci.yml/badge.svg)
![Python Version](https://img.shields.io/badge/python-3.10%2B-blue)
![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)
![License](https://img.shields.io/badge/license-MIT-green)

Biblioteca centralizada de automatización para mantenimiento operativo en Cloud (AWS/Azure) y On-Premise. Diseñada con principios de ingeniería de Software: modularidad, idempotencia y testing automatizado.

## Características

- **Arquitectura Modular:** Separación clara entre lógica de negocio (`src/ops_core`) y scripts de ejecución (`scripts/`).
- **Cloud Agnostic Design:** Módulos extensibles para AWS y Azure.
- **Calidad de Código:** Pipeline de CI/CD con GitHub Actions (Linting, Formatting, Unit Testing).
- **Documentación Viva:** Generación automática de docs técnicos con MkDocs.
- **Logging Estandarizado:** Trazabilidad completa de ejecuciones.

## Estructura del proyecto

```text
ops-automation/
├── config/              # Reglas de negocio (YAML/JSON)
├── docs/                # Documentación del proyecto (MkDocs)
├── scripts/             # Entrypoints y Wrappers Bash
├── src/
│   └── ops_core/        # Paquete principal Python
│       ├── aws/         # Lógica específica de AWS
│       ├── azure/       # Lógica específica de Azure
│       ├── common/      # Utilidades (Logging, Config Parser)
│       └── health/      # Verificaciones de estado
├── tests/               # Unit Tests (Pytest)
├── Makefile             # Comandos de gestión del proyecto
└── pyproject.toml       # Definición de dependencias y herramientas
```
## Quick Start

### Prerrequisitos
-   Python 3.9+
-   Make (Opcional, pero recomendado)

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
