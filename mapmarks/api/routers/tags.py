"""
@file:  mapmarks.api.routers.tags.py
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
    "prefix": "/tags",
    "tags": ['tags'],
    "responses": {404: {"description": "Oops. We could not find that."}}
}
tags = fastapi.APIRouter(**router_config)

# Tag Routing
@tags.get('/')
async def read_root():
    logger.debug(f"Received a Request for the Tags Router: /api/v1/tags/")
    return {"data": {"message": "Tags router"}}