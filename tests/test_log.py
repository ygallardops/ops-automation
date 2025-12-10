import logging
from ops_core.common.log import get_logger


def test_logger_creation():
    """Prueba que el logger se crea con el nombre y nivel correctos."""
    log_name = "test_module"
    logger = get_logger(log_name, level="DEBUG")

    # Verificaciones (Asserts)
    assert isinstance(logger, logging.Logger)
    assert logger.name == log_name
    assert logger.level == logging.DEBUG


def test_logger_singleton_behavior():
    """Prueba que no se duplican los handlers si llamamos a la funcion dos veces."""
    logger1 = get_logger("repeat_test")
    logger2 = get_logger("repeat_test")

    # Solo deberia tener 1 handler (el de consola), no 2.
    assert len(logger1.handlers) == 1
    assert logger1 is logger2
