"""
"""
from datetime import datetime as dt

from enum import Enum
from fastapi import FastAPI

from mapmarks.api.config import settings
from mapmarks.api.tags import Tag
from mapmarks.api.models.geojson import Feature


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
    
@app.post("/features/new", response_model=Feature, tags=[Tag.geolocations])
async def create_feature(feature: Feature):
    return feature.save()