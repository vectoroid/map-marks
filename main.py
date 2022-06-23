"""
file:  /main.py
        - entry script
        - required by Deta
"""

import typing

from datetime import datetime as dt
from uuid import UUID
from fastapi import Depends, FastAPI

from mapmarks.api.config import get_app_config
from mapmarks.api.tags import Tag
from mapmarks.api.models.geojson import Feature
from mapmarks.api.models.geojson import FeatureCollection
from mapmarks.api.exceptions import NotFoundHTTPException


# Set application configuration
settings = get_app_config()
app_config = {
    "debug": settings.debug_mode,
    "dependencies": [Depends(get_app_config)],
    "description": settings.description,
    "title": settings.title,
    "root_path": settings.root_path,
    "version": settings.version
}
# initialize app
app = FastAPI(**app_config)

# define MapMarkr routes
@app.get("/", response_model=list[Feature])
async def get_root():
    feature_list = await Feature.fetch()
    return feature_list
    
@app.get("/features")
async def list_features():
    return await Feature.fetch()

@app.get("/features/{feature_id}", response_model=Feature, tags=[Tag.geolocations])
async def find_feature(feature_id: typing.Union[UUID, str]):
    found_feature = await Feature.find(key=feature_id)
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
    
@app.delete("/features{feature_id}/delete", tags=[Tag.geolocations])
async def delete_feature(feature_id: int) -> None:
    return await Feature.delete()