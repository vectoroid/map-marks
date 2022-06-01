"""
GeoJSON models

-  defined iac with the [GeoJSON specification: RFC 7946](https://tools.ietf.org/html/rfc7946)
"""
import typing
from typing import List, Optional, Union
import uuid
from pydantic import confloat
from pydantic import validator

from mapmarks.api.models.base import DetaBase
from mapmarks.api.types import GeojsonType
from mapmarks.api.types import GeolocationCategory


# GeoJSON Position element
class Position(DetaBase):
    lon: confloat(gt=-180, lt=180)
    lat: confloat(gt=-90, lt=90)    
    
    @validator('lon')
    def lon_within_valid_range(cls, v):
        assert v in range(-180, 180), "Longitude value must be within the range: [-180, 180]"
        return v
    
    @validator('lat')
    def lat_within_valid_range(cls, v):
        assert v in range(-90, 90), "Latitude value must be within the range: [-90, 90]"
    
    def __repr__(self):
        return tuple(self.lon, self.lat)
    
    def __str__(self):
        self.__repr__()
        
    def __format__(self):
        return f"(lon={self.lon}, lat={self.lat})"


class Point(DetaBase):
    type: GeojsonType = "Point"
    coordinates: Position

    @validator("type")
    def type_must_be_valid(cls, v):
        if v is not "Point":
            error_msg = f"A GeoJSON Point object must have 'type'='Point'. You provided: 'type'='{v}'."
            raise ValueError( error_msg )
        
        return v


# Since the GeoJSON spec--[RFC7946](https://tools.ietf.org/html/rfc7946)--disallows arbitrary attributes/properties assigned to objects defined by the spec,
# it permits the three objects: `Feature`, `FeatureCollection`, and `GeometryCollection` to have an attributes, `properties`.
# *  the `properties` attribute is explicitly designed as a place to define any such arbitrary attributes. 
# *  we include, for instance, timestamps in `properties`, as well as a Feature's:
#    **  `name`
#    **  `notes`
#    **  `category`
class PropsInRequest(DetaBase):
    """
    """
    name: str
    note: typing.Optional[str]
    category: GeolocationCategory
class PropsInDb(PropsInRequest, TimestampMixin):
    """
    class: PropsInDb
    -  After receiving input, yet before saving this data to Deta Base,
       we need to add the following fields & corresponding values:
       *  created_at
       *  updated_at
    -  this endeavor is looked after by the TimestampMixin() class.
    """
    # all timestamping functionality is defined in the TimestampMixin() class
    pass
    

class FeatureInRequest(DetaBase):
    """
    """
    type: GeojsonType = "Feature"
    geometry: Point
    properties: PropsInRequest
    
    class Config:
        title: str = "Geolocation"
        
    @validator("type")
    def type_must_be_valid(cls, v):
        if v is not "Feature":
            error_msg = f"A GeoJSON 'Feature' object must have 'type'='Feature'; you provided: 'type'='{v}'."
            raise ValueError( error_msg )
        return v
        
class FeatureInDb(FeatureInRequest):
    """
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    properties: PropsInDb
    

class FeatureCollectionInRequest(DetaBase):
    """
    class FeatureCollectionInRequest
    -  items in `features` list are: FeatureInRequest() instances
    """
    type: str = GeojsonType.FEATURE_COLLECTION
    # features: typing.Union[typing.List[FeatureInRequest], typing.List[FeatureInDb], typing.List[None]]
    features: Union[List[FeatureInRequest], List[None]]
    
class FeatureCollectionInDb(FeatureCollectionInRequest):
    """
    class FeatureCollectionInDb
    -  items in `features` list are: FeatureInDb() instances
    """
    features: Union[List[FeatureInDb], List[None]]