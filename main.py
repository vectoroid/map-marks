"""
"""
from datetime import datetime as dt

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
from pydantic import confloat
from pydantic import validator
from pydantic import ValidationError

from mapmarks.api.config import settings
from mapmarks.api.tags import Tag
from mapmarks.api.models.geojson import FeatureInDb
from mapmarks.api.models.geojson import FeatureInRequest

# Set application configuration
app_config = {
    "debug": settings.debug_mode,
    "title": settings.title,
    "description": settings.description,
    "version": settings.version
}
# initialize app
app = FastAPI(**app_config)


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
            "created_at": dt.utcnow(),
            "payload": {"id": item_id, "type": "item"}
        }
    }
    
@app.post("/features/new", response_model=FeatureInDb, tags=[Tag.geolocations])
async def create_feature(feature: FeatureInRequest) -> FeatureInDb:
    try:
        return feature.save()
    except ValidationError as e:
        return (e.json())
    except Exception as e:
        print(e)