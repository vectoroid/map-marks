"""
MapMarkr app - save your place in life
"""

__version__ = "0.0.1"

# import app modules
from deta import Deta
from mapmarks.api.config import settings

# initialize Deta Base
deta = Deta()
async_db = deta.Base(settings.db_name)