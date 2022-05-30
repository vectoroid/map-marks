"""
GeoJSON models
"""
from pydantic import confloat
from pydantic import validator

from mapmarks.api.models.base import BaseModel
from mapmarks.api.types import GeojsonType
from mapmarks.api.types import GeolocationCategory


# GeoJSON Position element
class Position(BaseModel):
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


class Point(BaseModel):
    type: GeojsonType = "Point"
    coordinates: Position

    @validator("type")
    def type_must_be_valid(cls, v):
        if v is not "Point":
            error_msg = f"A GeoJSON Point object must have 'type'='Point'. You provided: 'type'='{v}'."
            raise ValueError( error_msg )
        
        return v


class PropsInRequest(BaseModel):
    """
    """
    name: str
    note: typing.Optional[str]
    category: GeolocationCategory
    
    
# class PropsInDb(PropsInRequest, TimestampMixin):
class PropsInDb(PropsInRequest):
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
    

class FeatureInRequest(BaseModel):
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
    id: GeolocationId = Field(default_factory=uuid.uuid4)
    properties: PropsInDb