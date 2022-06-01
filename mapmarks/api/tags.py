"""
"""
from enum import Enum


class Tag(Enum, str):
    """
    class Tag(Enum, str)
    
    -  These are tags for use in FastAPI (OpenAPI, really) -- 
       they're ultimately combined with & printed with the auto-generated API docs for the app
    -  These are not saved to the Deta Base.
    -  NOTE: if, in future, it becomes desirable and/or necessary to tag items in the Deta Base,
             be sure to CALL THEM SOMETHING ELSE.
    """
    geolocations: str = 'geolocations'
    users: str = 'users'