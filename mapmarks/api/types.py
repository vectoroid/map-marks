import enum
import typing


# App-specific types
GeolocationCategory = typing.Literal["Reefer", "Tobacco", "Other"]

# GeoJSON Types
class GeojsonType(str, enum.Enum):
    POINT = "Point"
    FEATURE = "Feature"
    FEATURE_COLLECTION = "FeatureCollection"
    

# Define geographical coordinates as generic types
Lon = typing.TypeVar('lon', bound=float)
Lat = typing.TypeVar('lat', bound=float)
