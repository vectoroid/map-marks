"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
from pydantic import BaseSettings, Extra


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
    """
    app_title: str = "MapMarkr"
    app_description: str = "Save your favorite places"
    app_version: str = "0.0.1"
    app_in_debug_mode: bool = True
    
    
    class Config:
        env_prefix = "DETA_"
        env_file = "../.env"
        extra = Extra.forbid