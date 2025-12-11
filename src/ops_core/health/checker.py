import time
import requests
from requests.exceptions import RequestException, Timeout, ConnectionError
from ops_core.common.log import get_logger

logger = get_logger(__name__)


def check_endpoint(name: str, url: str, timeout: int = 5) -> bool:
    """
    Realiza una peticion HTTP GET a una URL y mide su tiempo de respuesta.

    Returns:
        bool: True si el servicio responde 200 OK, False en caso contrario.
    """
    logger.info(f"Checking service: {name} ({url})...")
    start_time = time.time()

    try:
        response = requests.get(url, timeout=timeout)
        latency = (time.time() - start_time) * 1000  # Convertir a ms

        if response.status_code == 200:
            logger.info(
                f"[UP] {name} - Status: {response.status_code} "
                f"- Latency: {latency:.2f}ms"
            )
            return True
        else:
            logger.warning(
                f"[UNSTABLE] {name} returned status code {response.status_code}"
            )
            return False

    except Timeout:
        logger.error(f"[DOWN] {name} - Timed out after {timeout}s")
        return False

    except ConnectionError:
        logger.error(f"[DOWN] {name} - Connection refused (Is it running?)")
        return False

    except RequestException as e:
        logger.error(f"[DOWN] {name} - Unexpected error: {e}")
        return False


def run_checks(config: dict):
    """
    Ejecuta la suite de health checks basada en la configuracion.
    """
    monitor_config = config.get("monitor", {}).get("health_checks", {})
    targets = monitor_config.get("targets", [])
    timeout = monitor_config.get("timeout_seconds", 5)

    if not targets:
        logger.warning("No targets defined in config under monitor.health_checks")
        return

    logger.info(f"Starting Health Checks for {len(targets)} services...")

    success_count = 0
    for target in targets:
        name = target.get("name", "Unknown")
        url = target.get("url")

        if not url:
            logger.error(f"Target '{name}' has no URL configured. Skipping.")
            continue

        if check_endpoint(name, url, timeout):
            success_count += 1

    logger.info(
        f"Health Checks Completed. Success Rate: {success_count}/{len(targets)}"
    )
