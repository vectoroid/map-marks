"""
GeoJSON models

-  defined iac with the [GeoJSON specification: RFC 7946](https://tools.ietf.org/html/rfc7946)
"""
from code import interact
from datetime import datetime
from unicodedata import category

from pydantic import BaseModel
from pydantic import Field
# @todo Remove this import statement -- no longer needed
from pydantic import validator
from pydantic import root_validator
from typing import List
from typing import Optional
from typing import Tuple
from typing import Union
from uuid import UUID, uuid4

from mapmarks.api.config import AppSettings
from mapmarks.api.models.base import DetaBase, async_db_client
from mapmarks.api.types import GeojsonType
from mapmarks.api.types import GeolocationCategory
from mapmarks.api.types import Position

# init 
settings = AppSettings()

class Point(BaseModel):
    type: GeojsonType = Field(GeojsonType.POINT, const=True)
    coordinates: list[float]
    
    @validator("coordinates")
    def check_coordinates_length(cls, v):
        # validate length
        assert len(v) == 2, "The `coordinates` attribute should be a list of length 2, e.g. [longitude, latitude]"
        return v
        
    @validator("coordinates")
    def check_longitude_within_bounds(cls, v):
        # we should have: (-180.0 <= longitude <= 180.0)
        longitude = v[0]
        
        if longitude <= -180.0 or longitude >= 180.0:
            raise ValueError("Longitude must be within the range of: [-180.0, 180.0]")
        
        return v
    
    @validator("coordinates")
    def check_latitude_within_bounds(cls, v):
        # we should have: (-90.0 <= latitude <= 90.0)
        latitude = v[1]
        
        if latitude <= -90.0 or latitude >= 90.0:
            raise ValueError("Latitude must be within the range of: [-90.0, 90.0]")
        
        return v

class Props(BaseModel):
    """Represents the `properties` key in the GeoJSON spec. 
    
    A GeoJSON object can have custom/arbitrary attributes, not defined in the spec.
    """
    title: str
    note: Optional[str]
    category: GeolocationCategory
    version: int
    created: datetime = Field(default_factory=datetime.now, const=True) # should not change
    updated: datetime = Field(default_factory=datetime.now)

        
class Feature(DetaBase):
    """classFeature -- represents a GeoJSON Feature object (i.e. a place of interest on a map"""   
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: dict[type:GeojsonType.POINT, coordinates:list[float]]
    properties: Props
    class Config:
        title: str = "Geolocation"
        use_enum_values: bool = True # Use Enum.ITEM.value, rather than the raw Enum
        
    @validator("geometry")
    def check_coordinates(cls, v):
        assert len(v.coordinates) == 2, "Coordinates should be a list containing just two items: [longtitude, latitude]"
        
        longitude = v.coordinates[0]
        latitude = v.coordinates[1]
        
        if longitude <= -180.0 or longitude >= 180.0:
            raise ValueError("The first item in the `Feature.geometry.coordinates` list should be the Longitude value, between -180.0 and 180.0")

        if latitude <= -90.0 or latitude >= 90.0:
            raise ValueError("The second item in the `Feature.geometry.coordinates` list should be the Latitude value, between -90.0 and 90.0")
        
        return v
    


class FeatureCollection(BaseModel):
    """
    A class to represent a collection of Feature instances
    
    Attributes
    ----------
    features : List 
        A list whose items are: Feature() instances
    
    @todo: overload the `update()` and `delete()` instance methods. Anything else need to be refactored?
    """
    type: str = Field(GeojsonType.FEATURE_COLLECTION, const=True)
    features: Union[List[Feature], List[None]]
    
    class Config:
        title: str = "GeolocationCollection"
        use_enum_values: bool = True # Use Enum.ITEM.value, rather than the raw Enum
        

    async def save(self) -> List[DetaBase]:
        """Save this instance to Deta Base
        
        @note: it is necessary to overload the `save()` method in this class, because 
               the `super().save()` method is designed to deal with a single instance 
               per call, whereas the FeatureCollection class needs to iterate through
               the `Feature()` instances in their respective `features` list & save each
               one.
        """
        async with async_db_client(self.db_name) as db:
            saved_items = []
            
            for instance in self.features:
                instance.properties.version += 1
                saved_data = await db.put(instance.json())
                saved_items.append(Feature(**saved_data))
                
            return saved_items
    