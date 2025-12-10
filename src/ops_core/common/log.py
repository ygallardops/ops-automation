import logging
import sys

def get_logger(name: str, level: str = "INFO") -> logging.Logger:
    """
    Configura y retorna un logger estandarizado para la suite.
    
    Args:
        name (str): Nombre del módulo (usar __name__).
        level (str): Nivel de log (DEBUG, INFO, WARNING, ERROR).
        
    Returns:
        logging.Logger: Objeto logger configurado.
    """
    # Crear logger
    logger = logging.getLogger(name)
    
    # Evitar duplicar handlers si ya existen
    if logger.handlers:
        return logger
        
    logger.setLevel(level.upper())

    # Formato profesional: Timestamp | Nivel | Mensaje
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)-8s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Output a consola (stdout)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    logger.addHandler(console_handler)
    
    return logger
