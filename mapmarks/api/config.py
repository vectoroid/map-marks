"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
import math
from pydantic import BaseModel, BaseSettings, Field


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
    """
    title: str = "MapMarkr"
    description: str = "Save your favorite places"
    version: str = "0.0.1"
    debug_mode: bool = True
    db_name: str = Field('db_name', env="BASE_NAME")
    db_fetch_limit: int = Field(25, const=True)
        
    class Config:
        case_sensitive: bool = True
        env_prefix: str = "DETA_"
        env_file: str = "../../.env"
        
        
settings = AppSettings()