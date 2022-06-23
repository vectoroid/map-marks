"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
from functools import lru_cache
from pydantic import BaseSettings, Field


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
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
    # Logging config options
    
    # Meta config options
    class Config:
        env_file: str = "../../.env"
        env_prefix: str = "DETA_"
        
        
@lru_cache
def get_app_config() -> AppSettings:
    return AppSettings()