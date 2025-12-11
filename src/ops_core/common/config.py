import yaml
import os
from typing import Dict, Any


def load_config(config_path: str = "config/rules.yaml") -> Dict[str, Any]:
    """
    Carga la configuración desde un archivo YAML.

    Args:
        config_path (str): Ruta relativa al archivo de configuración.

    Returns:
        Dict: Diccionario con la configuración cargada.

    Raises:
        FileNotFoundError: Si el archivo no existe.
    """
    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found at: {config_path}")

    with open(config_path, "r") as file:
        try:
            return yaml.safe_load(file)
        except yaml.YAMLError as exc:
            raise ValueError(f"Error parsing YAML file: {exc}")
