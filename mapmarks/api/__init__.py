"""
MapMarkr app - save your place in life
"""

__version__ = "0.0.1"

# import app modules
from mapmarks.api.config import AppSettings
from mapmarks.api.types import Lon, Lat
from mapmarks.api.models.geojson import Point
from mapmarks.api.models.geojson import Props
from mapmarks.api.models.geojson import Feature
from mapmarks.api.models.geojson import FeatureCollection