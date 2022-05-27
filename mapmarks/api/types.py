import typing
import uuid


# GeoJSON Types
GeoJsonTypes = typing.Literal["Point", "Feature"] # not all GeoJSON types are used, presently
GeojsonCategory = typing.Literal["Reefer", "Tobacco"]

# Utility Types
Numeric = typing.Union[int, float]
GeolocationId = typing.NewType('GeolocationId', uuid.UUID)