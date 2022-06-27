"""
@file:  mapmarks.api.routers.features.py
@desc:  Builds a router (i.e. APIRouter == mini FastAPI class; has same PARAMS)

@summary
- from the `fastapi` Github repo, here is a record of the APIRouter() class parameters:

```
class APIRouter(routing.Router):
    def __init__(
        self,
        *,
        prefix: str = "",
        tags: Optional[List[Union[str, Enum]]] = None,
        dependencies: Optional[Sequence[params.Depends]] = None,
        default_response_class: Type[Response] = Default(JSONResponse),
        responses: Optional[Dict[Union[int, str], Dict[str, Any]]] = None,
        callbacks: Optional[List[BaseRoute]] = None,
        routes: Optional[List[routing.BaseRoute]] = None,
        redirect_slashes: bool = True,
        default: Optional[ASGIApp] = None,
        dependency_overrides_provider: Optional[Any] = None,
        route_class: Type[APIRoute] = APIRoute,
        on_startup: Optional[Sequence[Callable[[], Any]]] = None,
        on_shutdown: Optional[Sequence[Callable[[], Any]]] = None,
        deprecated: Optional[bool] = None,
        include_in_schema: bool = True,
        generate_unique_id_function: Callable[[APIRoute], str] = Default(
            generate_unique_id
        ),
```
    ) -> None:
"""
import fastapi
import logging


# Configure and crank up the Logger
logger = get_logger(__name__)

# Define Feature Router
router_config = {
    "prefix": "/features",
    "tags": ['features'],
    "responses": {404: {"description": "Oops. We could not find that."}}
}
features = fastapi.APIRouter(**router_config)

# Feature Routing
@features.get("/", response_model=list[Feature])
async def get_root():
    logger.info(f"Got a Request for this `APIRouter()'s` index route: /{}")
    logger.info("Retrieving list of MapMarkr Features currently saved to DB.")
    feature_list = await Feature.fetch()
    return feature_list
    
@features.get("/features")
async def list_features():
    return await Feature.fetch()

@features.get("/features/{feature_id}", response_model=Feature, tags=[Tag.geolocations])
async def find_feature(feature_id: typing.Union[UUID, str]):
    found_feature = await Feature.find(key=feature_id)
    if found_feature is None:
        raise NotFoundHTTPException
    return found_feature
    
@features.post("/features/new", tags=[Tag.geolocations])
async def create_feature(feature: Feature):
    new_feature = await feature.save()
    if new_feature is None or new_feature == '':
        raise NotFoundHTTPException
    return new_feature

@features.post("/features/{feature_id}/edit", tags=[Tag.geolocations])
async def update_feature(feature_id: int, payload: Feature):
    old_feature = await Feature.find(feature_id)
    
    if old_feature is None:
        raise NotFoundHTTPException
    
    old_feature.update(**payload.dict())
    
@features.delete("/features{feature_id}/delete", tags=[Tag.geolocations])
async def delete_feature(feature_id: int) -> None:
    return await Feature.delete()