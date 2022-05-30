"""
MapMarkr :: I/O Schema
- these schema are pydantic models (classes) which represent the application's
  I/O -- user input and app output, in the form of HTTPResponses, defined by 
  classes in FastAPI, or--more probably--Starlette.
"""
import typing
import uuid

from pydantic import Extra
from pydantic import confloat
from pydantic import validator
from pydantic import BaseModel as PydanticBase

from mapmarks.api.types import GeojsonType, GeolocationCategory, GeolocationId
# from mapmarks.api.interface import TimestampMixin

# Root subclass 
# -  simplest method to apply universal config options to all models
class BaseModel(PydanticBase):
    """
    class: mapmarks.api.schema.BaseModel
    module: mapmarks.api.schema
    
    note: Didn't realize I'd have a reason to create an intermediary class, between pydantic.BaseModel and
          my actual I/O models, so by renaming (effectively) pydantic.BaseModel to pydantic.PydanticBase, 
          I avoid having to replace all instances of 'BaseModel' throughout the app.
    """
    class Config:
        anystr_strip_whitespace: bool = True    # always strip whitespace from user-input strings
        extra: str = Extra.forbid
