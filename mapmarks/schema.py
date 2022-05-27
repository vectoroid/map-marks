"""
MapMarkr :: I/O Schema
- these schema are pydantic models (classes) which represent the application's
  I/O -- user input and app output, in the form of HTTPResponses, defined by 
  classes in FastAPI, or--more probably--Starlette.
"""
from pydantic import BaseModel


# GeoJSON Position element
class Position(BaseModel):
    """
    class Position
    - subclass of pydantic.BaseModel
    - NOTE: this is a component class -- it will not be included in app I/O
            directly, but rather as a component of other classes -- ultimately,
            (I think) the only actual I/O models will be the Feature() and 
            the FeatureCollection() classes; the rest will comprise those two.
    """
    lat: float
    long: float
        
        
class BaseFeature(BaseModel):
  """
  """
  type: str = 