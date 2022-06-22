"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
from pydantic import BaseSettings, Field


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
    """
    api_prefix: str = "/api/v1"
    title: str = "MapMarkr"
    description: str = "Save your favorite places"
    version: str = "0.0.1"
    debug_mode: bool = True
    db_name: str
    db_fetch_limit: int = Field(25, const=True)
        
    class Config:
        env_file: str = "../../.env"
        env_prefix: str = "DETA_"
        
        
settings = AppSettings()