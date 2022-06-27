"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
import logging
import os

from enum import Enum
from functools import lru_cache
from pydantic import BaseSettings, Field


# MapMarkr Operating Environment status
class OpEnviron(Enum):
    """class OperationEnvion
       - This class represents the App's operating environment: i.e. 'dev', 'staging' or 'production'.
       - These various environments are unlikely to change, and so should be "set in stone," so to speak.
         That is why it subclasses Enum.
    """
    dev = 'dev'
    staging = 'staging'
    production = 'production'
    

# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    Global app configuration/settings
    """
    # FastAPI config options
    root_path: str = "/api/v1"
    title: str = "MapMarkr"
    description: str = "Save your favorite places"
    version: str = "0.0.1"
    debug_mode: bool = True
    
    # DB config options
    db_name: str
    db_fetch_limit: int = Field(25, const=True)    
    
    # Logging config
    class Logging:
        encoding: str = 'utf-8'
        level: logging.WARN
        
        def __init__(self) -> None:
            self.__class__.set_level()
        
        @classmethod
        def set_level(cls):
            """Sets `logging.LEVEL` to the value of cls.debug_mode. Hopefully, this will be helpful if/when I deploy after forgetting to set an appropriate logging severity level."""
            c = get_app_config()
            return (cls.level := c.debug_mode)
                
    # Meta config options
    class Config:
        env_file: str = "../../.env"
        env_prefix: str = "DETA_"
        
    @property
    def operating_env(self) -> str:
        """
        Returns the app's operating environment -- e.g. 'dev', 'staging' (currently unused), or 'prod'. (property of AppSettings class)
        
        @NOTE: 
        The OperationEnviron.production environment is not yet available. 
        Until it is available, OperationEnviron.production will NOT be used.
        """

        if os.getenv("DETA_RUNTIME"):
            return OpEnviron.staging.value
        else:
            return OpEnviron.dev.value
            
        
        
        
@lru_cache
def get_app_config() -> AppSettings:
    return AppSettings()