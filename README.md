# Automatización operativa en Python y Bash

[![CI](https://github.com/ygallardops/ops-automation/actions/workflows/ci.yml/badge.svg)](https://github.com/ygallardops/ops-automation/actions/workflows/ci.yml)
[![Python 3.9+](https://img.shields.io/badge/python-3.9%2B-blue)](pyproject.toml)
[![Estilo: black](https://img.shields.io/badge/estilo-black-000000.svg)](https://github.com/psf/black)
[![Licencia MIT](https://img.shields.io/github/license/ygallardops/ops-automation)](LICENSE)

> **Laboratorio personal.** Son ejercicios de automatización operativa que escribo para practicar, no una herramienta mantenida ni un entregable profesional. Úsalo como referencia, no en producción.

Ejercicios de mantenimiento operativo para AWS y servidores on-premises, organizados como un paquete de Python con pruebas y CI.

## Qué hace

| Tarea | Qué hace | Cómo se ejecuta |
| --- | --- | --- |
| Limpieza de snapshots en AWS | Busca los snapshots de EC2 propios de la cuenta que superan la retención configurada. Por defecto solo los lista (`dry_run: true`) y se detiene si la cuenta no está en `allowed_account_ids`; si esa lista está vacía, omite la comprobación con una advertencia. | `make run-aws` |
| Verificación de salud HTTP | Consulta una lista de URL y registra cuáles responden y cuáles no. | `make run-monitor` |

Ambas tareas leen su configuración de [`config/rules.yaml`](config/rules.yaml) y escriben logs con un formato uniforme: fecha, nivel, módulo y mensaje. No hay módulo de Azure.

## Estructura

La lógica vive en un paquete de Python (`src/ops_core`) y los scripts de `scripts/` solo la invocan.

```text
ops-automation/
├── config/rules.yaml        # Retención, regiones, cuentas permitidas y URL a verificar
├── docs/                    # Documentación técnica (MkDocs)
├── scripts/                 # Scripts de Bash que preparan el entorno y llaman a Python
├── src/ops_core/
│   ├── aws/                 # Limpieza de snapshots de EC2
│   ├── common/              # Configuración y logging
│   └── health/              # Verificaciones HTTP
├── tests/                   # Pruebas unitarias con mocks (pytest)
├── Makefile                 # Atajos: install, test, lint, format, run-aws, run-monitor
└── pyproject.toml           # Paquete y configuración de herramientas
```

## Inicio rápido

Requisitos: Python 3.9 o superior (el CI prueba con 3.10) y una terminal Bash. En Windows, usa Git Bash o WSL. Make es opcional; la AWS CLI solo hace falta para ejecutar la limpieza contra una cuenta real, no para las pruebas.

```bash
git clone https://github.com/ygallardops/ops-automation.git
cd ops-automation
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
make install
make test
```

Los scripts de `scripts/` esperan el entorno virtual en `.venv`.

## Documentación

```bash
mkdocs serve
```

Luego abre `http://127.0.0.1:8000`.

## Antes de subir cambios

```bash
make format
make lint
make test
```

El CI ejecuta black, flake8 y pytest en cada push y pull request.

## Licencia

[MIT](LICENSE)
