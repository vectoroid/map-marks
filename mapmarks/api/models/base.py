"""
MapMarkr :: I/O Schema
- these schema are pydantic models (classes) which represent the application's
  I/O -- user input and app output, in the form of HTTPResponses, defined by 
  classes in FastAPI, or--more probably--Starlette.
"""
import contextlib
from email.policy import default
import fastapi
from uuid import UUID, uuid4

from aiohttp import ClientError
from typing import Any, Callable, ClassVar, Dict, List, Tuple, Union
from pydantic import Extra
from pydantic import Field
from pydantic import BaseModel
from pydantic import ValidationError

from mapmarks.api.config import AppSettings
from mapmarks.api.exceptions import NotFoundHTTPException


# init
from deta import Deta
deta = Deta()

settings = AppSettings()


@contextlib.asynccontextmanager
async def async_db_client(db_name: str):
    db_client = deta.AsyncBase(db_name)
    
    try:
        yield db_client
    except ClientError as e:
        print(e)
    finally:
        await db_client.close()
        

# Root subclass 
# -  simplest method to apply universal config options to all models
class DetaBase(BaseModel):
    """
    class: mapmarks.api.models.DetaBase
    module: mapmarks.api.models
    
    note: Didn't realize I'd have a reason to create an intermediary class, between pydantic.BaseModel and
          my actual I/O models, so by renaming (effectively) pydantic.BaseModel to pydantic.PydanticBase, 
          I avoid having to replace all instances of 'BaseModel' throughout the app.
          
    note: this is "heavily inspired by" (i.e. virtually plagiaristic in nature) the Monochrome API for Deta:
          
    """
    key: UUID = Field(default_factory=uuid4)
    db_name: ClassVar = Field(settings.db_name)
    
    class Config:
        """class mapmarks.api.models.base.DetaBase.Config
        """
        anystr_strip_whitespace: bool = True    # always strip whitespace from user-input strings
        # extra: str = Extra.forbid
        extra: str = Extra.allow

    
    async def save(self):
        async with async_db_client(self.db_name) as db:
            self.version += 1
            return await db.put(self.json()) # Deta will return the saved item, if operation is successful.

            
    async def update(self, *args, **kwargs):
        """
        DetaBase.update [instance method]
        
        -  (1) increment version number
        -  (2) create a new dict from the keyword args passed to me
        -  (3) update my own dict, rather than create a new instance just yet
        -  (4) send my data as JSON to Deta Base(), to save it.
        -  (5) return a new instance of myself, instantiated with data returned from Deta (hah)
        """
        async with async_db_client(self.db_name) as db:
            new_version = self.version + 1
            new_data = {**self.dict(), **kwargs, "version": new_version}
            self.__dict__.update(**new_data)
            
            saved_data = await db.put(self.json()) # Deta.Base.put() should return new record
            
            # return new instance, instantiated with the saved data returned from Deta.Base():
            return self.__class__(**saved_data)

            
            
    async def delete(self) -> None:
        """
        DetaBase.delete() instance method
        -  returns `None` because deta.Deta.Base and deta.Deta.AsyncBase 
           always return None from their respective delete() methods.
        """
        async with async_db_client(self.db_name) as db:
            await db.delete(str(self.key))
        
        return None
            
    @classmethod
    async def find(cls, key: Union[uuid.UUID, str], exception=NotFoundHTTPException) -> Union["DetaBase", None]:
        async with async_db_client(cls.db_name) as db:
            instance = await db.get(str(key))
            if instance is None and exception:
                raise exception
            elif instance:
                return cls(**instance)
            else:
                return None
            
    @classmethod
    async def fetch(cls, query, limit:int=settings.db_fetch_limit) -> List["DetaBase"]:
        async with async_db_client(cls.db_name) as db:
            query = fastapi.encoders.jsonable_encoder(query)
            results = db.fetch(query, limit=min(limit, settings.DB.fetch_limit))
            all_items = results.items
            
            while len(all_items) <= limit and results.last:
                results = db.fetch(query, last=results.last)
                all_items += results.items
                
            return [cls(**instance) for instance in all_items]
        
    @classmethod
    async def paginate(cls, query, limit:int, offset:int, order_by:Callable[["DetaBase"], str], do_reverse:bool=False) -> Tuple[int, List[Dict[str, Any]]]:
        if query is None:
            query = {}
            
        results = await cls.fetch(query, limit + offset)
        count = len(results)
        top = limit + offset
        page = sorted(results, key=order_by, reverse=do_reverse)[offset:top]
        
        return (count, page)
    
    @staticmethod
    async def delete_many(instances: List["DetaBase"]) -> str:
        for instance in instances:
            await instance.delete()
            
        return "OK"