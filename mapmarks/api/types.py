import typing
import uuid

# App-specific types
GeolocationCategory = typing.Literal["Reefer", "Tobacco"]

# GeoJSON Types
GeolocationId = typing.NewType('GeolocationId', uuid.UUID)
GeojsonType = typing.Literal["Point", "Feature"] # not all GeoJSON types are used, presently