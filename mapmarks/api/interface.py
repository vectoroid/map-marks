"""
file: /mapmarks/api/interface.py

These are definitions of Mix-in classes -- essentially, this is the conventional way to implement 
the OOP concept of Interfaces in Python; these "classes" contain only specific functionality, and 
their subclasses inherit just those specific functionalities, ultimately allowing you to add "behaviors" 
to arbitrary classes.
"""
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

try:
    import async_db
except ImportError as import_err:
    print(import_err)
    pass


class TimestampMixin:
    """
    class: TimestampMixin
    notes: -  bestows `timestamp` behavior on classes which incorporate this mixin 
              (i.e. subclass this class)
    """
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)