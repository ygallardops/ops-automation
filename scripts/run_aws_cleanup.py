import sys
import os

# Agregamos 'src' al path para poder importar nuestros modulos
sys.path.append(os.path.join(os.path.dirname(__file__), "../src"))

from ops_core.common.config import load_config  # noqa: E402
from ops_core.aws.snapshots import cleanup_snapshots  # noqa: E402


def main():
    try:
        # 1. Cargar configuracion
        config = load_config("config/rules.yaml")

        # 2. Ejecutar logica
        cleanup_snapshots(config)

    except Exception as e:
        print(f"Critical Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
