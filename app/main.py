from fastapi import FastAPI

from app.api import register_routers
from app.settings import get_settings


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function initializes the FastAPI app with values from config,
    registers all routers, and returns the app instance for use
    by an ASGI server like Uvicorn.

    Returns:
        FastAPI: A configured FastAPI application instance.
    """
    settings = get_settings()

    app = FastAPI(
        title=settings.fastapi.title,
        description=settings.fastapi.description,
        version=settings.fastapi.version,
        docs_url=settings.fastapi.docs_url,
        redoc_url=settings.fastapi.redoc_url,
        openapi_url=settings.fastapi.openapi_url,
        debug=settings.fastapi.debug,
    )

    register_routers(app)
    return app


# ASGI app instance for use with Uvicorn or Hypercorn
app = create_app()
