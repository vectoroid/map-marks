"""
MapMarkr app - save your place in life
"""

__version__ = "0.0.1"

# import app modules
from mapmarks.api.config import AppSettings
from mapmarks.api.models.geojson import Position
from mapmarks.api.models.geojson import Point
from mapmarks.api.models.geojson import FeatureInRequest
from mapmarks.api.models.geojson import FeatureInDb
from mapmarks.api.models.geojson import FeatureCollectionInRequest
from mapmarks.api.models.geojson import FeatureCollectionInDb
from mapmarks.api.models.geojson import PropsInRequest
from mapmarks.api.models.geojson import PropsInDb