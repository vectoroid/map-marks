import typing
import uuid

# App-specific types
GeolocationCategory = typing.Literal["Reefer", "Tobacco"]

# GeoJSON Types
GeojsonType = typing.Literal["Point", "Feature"] # not all GeoJSON types are used, presently