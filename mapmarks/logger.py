"""module: logger.py

    - purpose:  In order to reduce repetitive code, since each module in the app will need a logger,
                this module encapsulates all code needed to produce a configured logger with the name 
                value set equal to the module's __name__ variable's value.
"""
import logging

from functools import lru_cache
from pathlib import PurePath
from mapmarks.api.config import get_app_config, OperationEnviron

# Get app configuration settings
settings = get_app_config()    

def get_logger(logger_name: str) -> logging.Logger:
    """Gets the appropriate logger by name, or initialises a new Logger. Returns logging.Logger."""
    logging_level: int
    
    # determine which logging.LEVEL should be used
    if settings.operating_env == OperationEnviron.staging.value:
        logging_level = logging.INFO
    elif settings.operating_env == OperationEnviron.dev.value:
        logging_level = logging.DEBUG
    
    # configure logger
    logger_config = {
        # @NOTE: the following line is commented out, 
        #        because the Deta.sh filesystem is READ-ONLY.
        # "filename": str(PurePath(f"./logs/{logger_name}.log")),
        "encoding": 'utf-8',
        "level": logging_level
    }
    logging.basicConfig(**logger_config)
    
    # Instantiate logger with the name provided
    return logging.getLogger(logger_name)