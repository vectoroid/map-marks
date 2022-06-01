"""
MapMarkr :: I/O Schema
- these schema are pydantic models (classes) which represent the application's
  I/O -- user input and app output, in the form of HTTPResponses, defined by 
  classes in FastAPI, or--more probably--Starlette.
"""
import aiohttp
import contextlib
import fastapi
import math
import typing
import uuid

from pydantic import Extra
from pydantic import Field
from pydantic import BaseModel

from mapmarks.api.config import AppSettings
from mapmarks.api.interfaces import TimestampMixin


# init
from deta import Deta
deta = Deta()

settings = AppSettings()

# 
@contextlib.asynccontextmanager
async def async_db_client(db_name: str):
    db_client = deta.AsyncBase(db_name)
    
    try:
        yield db_client
    except aiohttp.ClientError as e:
        print(e)
    finally:
        await db_client.close()
        

# Root subclass 
# -  simplest method to apply universal config options to all models
class DetaBase(BaseModel, TimestampMixin):
    """
    class: mapmarks.api.schema.DetaBase
    module: mapmarks.api.schema
    
    note: Didn't realize I'd have a reason to create an intermediary class, between pydantic.BaseModel and
          my actual I/O models, so by renaming (effectively) pydantic.BaseModel to pydantic.PydanticBase, 
          I avoid having to replace all instances of 'BaseModel' throughout the app.
          
    note: this is "heavily inspired by" (i.e. virtually plagiaristic in nature) the Monochrome API for Deta:
          
    """
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
    version: int = 1
    db_name: typing.ClassVar
    
    class Config:
        """
        class mapmarks.api.models.base.DetaBase.Config
        
        attributes:
        - anystr_strip_whitespace: bool
          strips whitespace from any strings assigned to model (and subclasses) attributes
        - extra: str
          * what to do if user attempts to add additional (i.e. extra) attributes to 
            this model or its subclasses -- other than those defined here?
          * can be Extra.allow, Extra.forbid, or Extra.ignore
            **  allow = allow extra, arbitrary/unlimited number of additonal model attributes
            **  forbid = expressly forbid addtional/extra attributes; will cause validation to 
                  fail if/when any extra attributes are assigned to this model or its subclasses.
            **  ignore = silently ignore and discard any additional attributes
        """
        anystr_strip_whitespace: bool = True    # always strip whitespace from user-input strings
        extra: str = Extra.forbid
        
    def dict(self, *args, **kwargs) -> dict:
        """
        Inject `key` attribute into self.dict() view
        
        - Why is it necessary to overload object.dict?
          *  because Deta uses `key` rather than `id` as the "primary key" in their databases; one must 
             either provide a valid key or accept Deta's default key value. So, if you choose to provide 
             your own, then overloading `dict` is necessary.
        """
        return {**super().dict(*args, **kwargs), "key": str(self.id)}
    
    async def save(self):
        async with async_db_client(self.db_name) as db:
            self.version += 1
            await db.put(self.json())
            
    async def update(self, *args, **kwargs):
        async with async_db_client(self.db_name) as db:
            new_version = self.version + 1
            new_props = {**self.dict(), **kwargs, "version": new_version}
            new_instance = self.__class__(**new_props)
            await db.put(new_instance.json())
            
    async def delete(self):
        async with async_db_client(self.db_name) as db:
            await db.delete(str(self.id))
            
    @classmethod
    async def find(cls, _id: typing.Union[uuid.UUID, str], exception=fastapi.HTTPException):
        async with async_db_client(cls.db_name) as db:
            instance = await db.get(str(_id))
            if instance is None and exception:
                raise exception
            elif instance:
                return cls(**instance)
            else:
                return None
            
    @classmethod
    async def fetch(cls, query, limit:int=math.inf):
        async with async_db_client(cls.db_name) as db:
            query = fastapi.encoders.jsonable_encoder(query)
            results = db.fetch(query, limit=min(limit, settings.DB.fetch_limit))
            all_items = results.items
            
            while len(all_items) <= limit and results.last:
                results = db.fetch(query, last=results.last)
                all_items += results.items
                
            return [cls(**instance) for instance in all_items]