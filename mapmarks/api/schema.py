"""
MapMarkr :: I/O Schema
- these schema are pydantic models (classes) which represent the application's
  I/O -- user input and app output, in the form of HTTPResponses, defined by 
  classes in FastAPI, or--more probably--Starlette.
"""
from pydantic import BaseModel


# GeoJSON Position element
class Position(BaseModel):
    lon: confloat(gt=-180, lt=180)
    lat: confloat(gt=-90, lt=90)    
    
    @validator('lon')
    def lon_within_valid_range(cls, v):
        assert v in range(-180, 180), "Longitude value must be within the range: [-180, 180]"
        return v
    
    @validator('lat')
    def lat_within_valid_range(cls, v):
        assert v in range(-90, 90), "Latitude value must be within the range: [-90, 90]"
    
    def __repr__(self):
        return tuple(self.lon, self.lat)
    
    def __str__(self):
        self.__repr__()
        
    def __format__(self):
        return f"(lon={self.lon}, lat={self.lat})"