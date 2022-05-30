"""
MapMarkr -- Configuration

This file contains application-wide settings -- e.g. database name, etc.
-  uses Pydantic's BaseSettings class to incorporate sophisticated 
   settings mapanagement for MapMarkr.
"""
import os
from pydantic import BaseSettings, Field


# MapMarkr settings-management class
class AppSettings(BaseSettings):
    """
    App-wide configuration/settings
    """
    app_title: str = "MapMarkr"
    app_description: str = "Save your favorite places"
    app_version: str = "0.0.1"
    app_in_debug_mode: bool = True
    
    class DB(BaseSettings):
        """
        """    
        name: str = Field(..., env="BASE_NAME")
        
    class Config:
        case_sensitive: bool = True
        env_prefix: str = "DETA_"
        env_file: str = "../../.env"
