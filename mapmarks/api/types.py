import datetime as dt
import typing
import uuid


# GeoJSON Types
Lon = typing.NewType("Lon", "float")    # Longitude (i.e. Position.x)
Lat = typing.NewType("Lat", "float")    # Latitude (i.e. Position.y)

# Utility Types
Numeric = typing.Union[int, float]
GeolocationId = typing.NewType('GeolocationId', uuid.UUID)