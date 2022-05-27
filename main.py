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
    id: GeolocationId = Field(default_factory=uuid.uuid4)
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
    