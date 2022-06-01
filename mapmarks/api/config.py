"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
import math
from pydantic import BaseSettings, Field


class DBSettings(BaseSettings):
    """
    """
    name: str = Field(..., env="BASE_NAME")
    max_fetch_limit: int = Field(25, const=True)


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
    """
    title: str = "MapMarkr"
    description: str = "Save your favorite places"
    version: str = "0.0.1"
    debug_mode: bool = True
    DB: DB = DB()
        
    class Config:
        case_sensitive: bool = True
        env_prefix: str = "DETA_"
        env_file: str = "../../.env"
        
        
settings = AppSettings()