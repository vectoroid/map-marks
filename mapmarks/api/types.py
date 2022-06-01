import enum
import typing


# App-specific types
GeolocationCategory = typing.Literal["Reefer", "Tobacco", "Other"]

# GeoJSON Types
class GeojsonType(enum.Enum, str):
    POINT = "Point"
    FEATURE = "Feature"
    FEATURE_COLLECTION = "FeatureCollection"