"""
"""
# from deta import Deta
import datetime as dt
import typing
import uuid

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(debug=True)

# APP SCHEMA
### Types
Props = dict[str, typing.Union[str, dt.datetime]]

### Schema Models
class LocationType(str, Enum):
    reefer: str = "Reefer"
    tobacco: str = "Tobacco"
    
class BaseProps(BaseModel):
    name: str
    notes: typing.Optional[str]
    category: LocationType
    
class PropsInDb(BaseProps):
    created_at: dt.datetime = Field()
    
class Position:
    lon: float
    lat: float
    
class Point(BaseModel):
    type: str = "Point"
    coordinates: Position
    
class FeatureInRequest(BaseModel):
    type: str = "Feature"
    geometry: Point
    properties: Props
    
class FeatureInDb(FeatureInRequest):
    id: uuid.UUID
    properties: Props

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