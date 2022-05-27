"""
file: /mapmarks/api/interface.py

These are definitions of Mix-in classes -- essentially, this is the conventional way to implement 
the OOP concept of Interfaces in Python; these "classes" contain only specific functionality, and 
their subclasses inherit just those specific functionalities, ultimately allowing you to add "behaviors" 
to arbitrary classes.
"""
from datetime import datetime

from deta import Deta
from pydantic import BaseModel, Field


class TimestampMixin(object):
    """
    class: TimestampMixin

    -  bestows "timestamping" behavior/mixin upon subclasses.
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    
class DetaBaseMixin(object):
    """
    class: DetaBaseMixin
    -  currently just a stub
    """
    def save(self):
        raise NotImplemented
    
    def update(self):
        raise NotImplemented
    
    def delete(self):
        raise NotImplemented