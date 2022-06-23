"""
GeoJSON models

-  defined IAC with the [GeoJSON specification: RFC 7946](https://tools.ietf.org/html/rfc7946)
"""


from datetime import datetime

from pydantic import BaseModel
from pydantic import Field
from pydantic import validator
from typing import List
from typing import Optional
from typing import NamedTuple
from typing import Union
from uuid import UUID, uuid4

from mapmarks.api.config import AppSettings
from mapmarks.api.models.base import DetaBase, async_db_client
from mapmarks.api.types import GeojsonType
from mapmarks.api.types import GeolocationCategory
from mapmarks.api.types import Lon, Lat

# init 
settings = AppSettings()

class Position(NamedTuple):
    lon: Lon
    lat: Lat


class Point(BaseModel):
    type: GeojsonType = Field(GeojsonType.POINT, const=True)
    coordinates: Position
    
    class Config:
        schema_extra = {
            "example": {
                "type": GeojsonType.POINT,
                "coordinates": [Lon, Lat]
            }
        }
    
    @validator("coordinates", allow_reuse=True)
    def check_coordinates(cls, v):
        if len(v) != 2:
            raise ValueError("The coordinates attribute must have a magnitude (length) of 2 items: [longitude, latitiude]")
        
        lon = v[0]
        lat = v[1]
        
        if lon <= -180.0 or lon >= 180.0:
            raise ValueError("Longitude must be no less than -180.00 and no more than 180.0.")
        
        if lat <= -90.0 or lat >= 90.0:
            raise ValueError("Latitude must be no less than -90.0 and no more than 90.0")
        
        return v

    

class Props(BaseModel):
    """Represents the `properties` key in the GeoJSON spec. 
    
    A GeoJSON object can have custom/arbitrary attributes, not defined in the spec.
    """
    title: str  # this is the 'title' of the record in Deta Base
    note: Optional[str]
    category: GeolocationCategory
    created: datetime = Field(default_factory=datetime.now) # should not change
    updated: datetime = Field(default_factory=datetime.now)
    version: Optional[int] = Field(0)
    
    class Config:
        underscore_attrs_are_private: bool = True
    
    def increment_version(self) -> int:
        """Props.increment_version -- adds 1 to the value of Props.version
           -  needed when saving and updating instances of this model
        """
        self.version += 1
        return self.version

        
class Feature(DetaBase):
    """class Feature -- represents a GeoJSON Feature object (i.e. a place of interest on a map"""   
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: Point
    properties: Props
    class Config:
        title: str = "Geolocation" # This is the title for this resource, as represented by Open API
        use_enum_values: bool = True # Use Enum.ITEM.value, rather than the raw Enum
        schema_extra = {
            "example": {
                "type": GeojsonType.FEATURE,
                "geometry": {
                    "type": GeojsonType.POINT,
                    "coordinates": [Lon, Lat]
                },
                "properties": {
                    "title": "South Beach Lifeguard Station",
                    "category": "Other",
                    "created": "2023-01-01T11:01:18.588438",
                    "updated": "2023-01-01T11:01:18.588438",
                    "version": 3
                }
            }
        }
    


class FeatureCollection(BaseModel):
    """
    A class to represent a collection of Feature instances
    
    @TODO: Is this class necessary? Not as an Input Schema/Model (pydantic), I wouldn't think. 
           I don't anticipate offering an endpoint at which users can submit multiple features at once.
           The most likely use case I see for FeatureCollection objects (i.e. the GeoJSON FC object; not 
           this class) is when returning multiple features from any endpoints (now or in future) which 
           allow the user to query the DB. If multiple Features are found based on a query, then it would 
           make sense to return them as a GeoJSON FeatureCollection -- but is a distinct class necessary for that?
           (1)  It could conceivably be done through the endpoint function: just wrap the queried Feature 
                objects in a dict with a 'type' key and a 'features' key; e.g.:
                    {"type": "FeatureCollection", "features": [...]}
            (2) On the other hand, this might lead to several issues as the codebase grows:
                - violates the "Separation of Concerns" paradigm -- resulting in tightly coupled code (BAD)
                - Without a Pydantic ResponseModel, you'll lose the advantages Pydantic offers.
    
    Attributes
    ----------
    features : List 
        A list whose items are: Feature() instances
    
    @todo: overload the `update()` and `delete()` instance methods. Anything else need to be refactored?
    """
    type: str = Field(GeojsonType.FEATURE_COLLECTION, const=True)
    features: Union[List[Feature], List[None]]
    
    class Config:
        title: str = "Feature Collection"
        use_enum_values: bool = True # Use Enum.ITEM.value, rather than the raw Enum
        

    async def save(self) -> List[Feature]:
        """Save this instance to Deta Base
        
        @note: it is necessary to overload the `save()` method in this class, because 
               the `super().save()` method is designed to deal with a single instance 
               per call, whereas the FeatureCollection class needs to iterate through
               the `Feature()` instances in their respective `features` list & save each
               one.
        """
        async with async_db_client(settings.db_name) as db:
            saved_items = []
            
            for instance in self.features:
                instance.properties.version += 1
                saved_data = await db.put(instance.json())
                saved_items.append(Feature(**saved_data))
                
            return saved_items
    