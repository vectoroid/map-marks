"""
"""
# from deta import Deta
import datetime as dt
import typing
import uuid

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
# from pydantic import ValidationError
from pydantic import confloat
from pydantic import validator

from mapmarks.api.config import AppSettings
from mapmarks.api.types import GeolocationCategory, GeoJsonTypes, GeolocationId

# Set application configuration
appconf = AppSettings()
app_config_params = {
    "debug": appconf.app_in_debug_mode,
    "title": appconf.app_title,
    "description": appconf.app_description,
    "version": appconf.app_version
}
# initialize app
app = FastAPI(**app_config_params)


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
    
    
class BaseProps(BaseModel):
    name: str
    notes: typing.Optional[str]
    
    
class PropsInput(BaseProps):
    category: GeolocationCategory
  
    
class PropsOutput(PropsInput):
    created_at: dt.datetime = Field()

    
class Point(BaseModel):
    type: str = "Point"
    coordinates: Position


class FeatureInRequest(BaseModel):
    type: str = "Feature"
    geometry: Point
    properties: PropsInput
    
    
class FeatureInDb(FeatureInRequest):
    id: uuid.UUID
    properties: PropsOutput


# define MapMarkr routes
@app.get("/")
async def get_root():
    return {
        "data": {"payload": "Hello, world!"}
    }

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {
        "data": {
            "created_at": dt.datetime.now(),
            "payload": {"id": item_id, "type": "item"}
        }
    }
    