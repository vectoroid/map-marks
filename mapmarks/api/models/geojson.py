"""
GeoJSON models

-  defined iac with the [GeoJSON specification: RFC 7946](https://tools.ietf.org/html/rfc7946)
"""
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

        
class Feature(DetaBase):
    """classFeature -- represents a GeoJSON Feature object (i.e. a place of interest on a map"""   
    type: GeojsonType = Field(GeojsonType.FEATURE, const=True)
    geometry: dict(type=GeojsonType.POINT, coordinates=list[float])
    properties: dict(
        title: str, 
        note: Optional[str], 
        category: GeolocationCategory, 
        version: int = 1,
        created: datetime = Field(default_factory=datetime.utcnow),
        updated: datetime = Field(default_factory=datetime.utcnow)
    ) 
    class Config:
        title: str = "Geolocation"
        use_enum_values: bool = True # Use Enum.ITEM.value, rather than the raw Enum
    


class FeatureCollection(DetaBase):
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

    async def save(self) -> List["DetaBase"]:
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
                instance.version += 1
                saved_data = await db.put(instance.json())
                saved_items.append(Feature(**saved_data))
                
            return saved_items
    