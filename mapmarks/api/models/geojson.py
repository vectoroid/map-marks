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
    

class FeatureInRequest(DetaBase):
    """
    """
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: Point
    properties: PropsInRequest
    
    class Config:
        title: str = "Geolocation"
        
    @validator("type")
    def type_must_be_valid(cls, v):
        valid_type = GeojsonType.FEATURE.value
        
        if v is not valid_type:
            error_msg = f"A GeoJSON '{valid_type}' object must have 'type'='{valid_type}'; you provided: 'type'='{v}'."
            raise ValueError( error_msg )
        return v
        
class FeatureInDb(DetaBase):
    """Represents a [GeoJSON] Feature object which has been saved to Deta Base.
    
    Attributes
    ----------
    type : GeojsonType
        The specific type of GeoJSON object this is (a `Feature` object, in this case.)
    
    geometry : Point
        The geometry attribute is meant to be one of an enumerated list of geometric types
        (e.g. Point, Line, MultiPoint, MultiLine, various shapes); 

        However, for this app, I anticipate needing only the Point geometric object.
        
    properties : PropsInDb
        These are the user-defined, application-specific properties (i.e. metadata) that shall be attached 
        to a particular instance of this class.
    """
    type: GeojsonType = Field(GeojsonType.FEATURE.name, const=True)
    geometry: Point
    properties: PropsInDb
    
    class Config:
        title: str = "Geolocation"
        
    # Is this custom validator even necessary? I mean, shouldn't Pydantic catch a bad `type` input,
    # based on the attribute type and Field definitions?
    #
    # @validator("type")
    # def type_must_be_valid(cls, v):
    #     valid_type = GeojsonType.FEATURE.value
        
    #     if v is not valid_type:
    #         error_msg = f"A GeoJSON '{valid_type}' object must have 'type'='{valid_type}'; you provided: 'type'='{v}'."
    #         raise TypeError( error_msg )
    #     return v
    

class FeatureCollectionInRequest(DetaBase):
    """
    A class to represent a collection of FeatureInRequest instances
    
    Attributes
    ----------
    features : List 
        A list whose items are: FeatureInRequest() instances
    
    @todo: overload the `update()` and `delete()` instance methods. Anything else need to be refactored?
    """
    type: str = Field(GeojsonType.FEATURE_COLLECTION.value, const=True)
    features: Union[List[FeatureInRequest], List[None]]
    
    class Config:
        title: str = "GeolocationCollection"
        
    @validator("type")
    def type_must_be_valid(cls, v):
        valid_type = GeojsonType.FEATURE_COLLECTION.value
        
        if v is not valid_type:
            error_msg = f"A GeoJSON '{valid_type}' object must have 'type'='{valid_type}'; you provided: 'type'='{v}'."
            raise TypeError(error_msg)
        
        return v

    
    async def save(self) -> List[self.__class__.__name__]:
        """Save this instance to Deta Base
        
        @note: it is necessary to overload the `save()` method in this class, because 
               the `super().save()` method is designed to deal with a single instance 
               per call, whereas all FeatureCollection* classes need to iterate through
               the `Feature()` instances in their respective `features` list & save each
               one.
        """
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