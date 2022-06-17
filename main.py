"""
"""
from datetime import datetime as dt
import typing
from fastapi import FastAPI

from mapmarks.api.config import settings
from mapmarks.api.tags import Tag
from mapmarks.api.models.geojson import Feature
from mapmarks.api.exceptions import NotFoundHTTPException


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
    features = await Feature.fetch()
    return dict(metadata={"payload": "Hello, world!"}, data=features)
    
@app.get("/features")
async def list_features() -> typing.List:
    return await Feature.fetch()

@app.get("/features/{feature_id}")
async def find_feature(fid: int) -> Feature:
    found_feature = await Feature.find(key=fid)
    if found_feature is None:
        raise NotFoundHTTPException
    return found_feature
    
@app.post("/features/new", tags=[Tag.geolocations])
async def create_feature(feature: Feature):
    new_feature = await feature.save()
    if new_feature is None or new_feature == '':
        raise NotFoundHTTPException
    return new_feature

@app.post("/features/{feature_id}/edit", tags=[Tag.geolocations])
async def update_feature(feature_id: int, payload: Feature):
    old_feature = await Feature.find(feature_id)
    
    if old_feature is None:
        raise NotFoundHTTPException
    
    old_feature.update(**payload.dict())