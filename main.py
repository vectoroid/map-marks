"""
"""
# from deta import Deta
from datetime
from datetime import datetime as dt

from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel
from pydantic import Field
from pydantic import confloat
from pydantic import validator

from mapmarks.api.config import AppSettings

# Set application configuration
appconf = AppSettings()
app_config_params = {
    "debug": appconf.app_in_debug_mode,
    "title": appconf.app_title,
    "description": appconf.app_description,
    "version": appconf.app_version
}
# initialize app
app = FastAPI(**app_config_params)


# define MapMarkr routes
@app.get("/")
async def get_root():
    return {
        "data": {"payload": "Hello, world!"}
    }

@app.get("/items/{item_id}")
async def get_item(item_id: int):
    return {
        "data": {
            "created_at": dt.utcnow(),
            "payload": {"id": item_id, "type": "item"}
        }
    }
    