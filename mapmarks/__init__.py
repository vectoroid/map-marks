"""
MapMarkr app - save your place in life
"""

__version__ = "0.0.1"

# import app modules
from deta import Deta
from mapmarks.api.config import get_app_config

# Get app config settings
settings = get_app_config()
