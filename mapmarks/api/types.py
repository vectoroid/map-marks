import enum
import typing
import typing_extensions
import uuid

# App-specific types
GeolocationCategory = typing.Literal["Reefer", "Tobacco"]

# GeoJSON Types
class GeojsonType(enum.Enum, str):
    POINT = "Point"
    FEATURE = "Feature"
    FEATURE_COLLECTION = "FeatureCollection"