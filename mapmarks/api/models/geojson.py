"""
GeoJSON models

-  defined iac with the [GeoJSON specification: RFC 7946](https://tools.ietf.org/html/rfc7946)
"""
from pydantic import BaseModel
from pydantic import confloat
from pydantic import Field
from pydantic import validator
from typing import List, Optional, Union
from uuid import UUID, uuid4

from mapmarks.api.config import AppSettings
from mapmarks.api.models.base import DetaBase, async_db_client
from mapmarks.api.interfaces import TimestampMixin
from mapmarks.api.types import GeojsonType
from mapmarks.api.types import GeolocationCategory

# init 
settings = AppSettings()

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
    """
    class Point
    
    -  NOTE: no `id` or `key` attribute needed -- this model will be nested within the 
             Feature* classes.
    """
    type: GeojsonType = Field(GeojsonType.POINT, const=True)
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
class PropsInRequest(BaseModel):
    """
    """
    name: str
    note: Optional[str]
    category: GeolocationCategory
    
class PropsInDb(PropsInRequest, TimestampMixin):
    """
    class: PropsInDb
    -  NOTE: this class needs no `id` or `key` attribute, because it is not saved to 
             Deta Base directly--it is a "sub-model" of the Feature* classes.
    
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
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: Point
    properties: PropsInRequest
    
    class Config:
        title: str = "Geolocation"
        
    @validator("type")
    def type_must_be_valid(cls, v):
        if v is not "Feature":
            error_msg = f"A GeoJSON 'Feature' object must have 'type'='{GeojsonType.FEATURE}'; you provided: 'type'='{v}'."
            raise ValueError( error_msg )
        return v
        
class FeatureInDb(DetaBase):
    """
    """
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: Point
    properties: PropsInDb
    
    class Config:
        title: str = "Geolocation"
        
    @validator("type")
    def type_must_be_valid(cls, v):
        if v is not "Feature":
            error_msg = f"A GeoJSON 'Feature' object must have 'type'='{GeojsonType.FEATURE}'; you provided: 'type'='{v}'."
            raise ValueError( error_msg )
        return v
    

class FeatureCollectionInRequest(DetaBase):
    """
    class FeatureCollectionInRequest
    -  items in `features` list are: FeatureInRequest() instances
    
    @todo: overload the `update()` and `delete()` instance methods. Anything else need an update?
    """
    type: str = Field(GeojsonType.FEATURE_COLLECTION, const=True)
    features: Union[List[FeatureInRequest], List[None]]
    
    async def save(self) -> List[self.__class__]:
        async with async_db_client(self.db_name) as db:
            saved_items = []
            
            for instance in self.features:
                instance.version += 1
                saved_data = await db.put(instance.json())
                saved_items.append(self.__class__(**saved_data))
                
            return saved_items
    
class FeatureCollectionInDb(FeatureCollectionInRequest):
    """
    class FeatureCollectionInDb
    -  items in `features` list are: FeatureInDb() instances
    """
    features: Union[List[FeatureInDb], List[None]]