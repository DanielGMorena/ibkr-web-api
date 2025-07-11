from typing import Optional

from fastapi import FastAPI

from app.api import register_routers
from app.settings import get_settings


def create_app(config_path: Optional[str] = None) -> FastAPI:
    """
    Application factory for creating and configuring a FastAPI app.

    This function initializes the FastAPI app using settings from a configuration
    file (YAML) and environment variables. It also registers all routers for the API.

    Args:
        config_path (Optional[str]): Optional path to a YAML config file.
            If not provided, defaults to the value of the APP_CONFIG environment
            variable or 'config.yml'.

    Returns:
        FastAPI: A fully configured FastAPI application instance.
    """
    # Load application settings (from YAML + .env)
    settings = get_settings(config_path)

    # Create FastAPI app using settings
    app = FastAPI(
        title=settings.fastapi.title,
        description=settings.fastapi.description,
        version=settings.fastapi.version,
        docs_url=settings.fastapi.docs_url,
        redoc_url=settings.fastapi.redoc_url,
        openapi_url=settings.fastapi.openapi_url,
        debug=settings.fastapi.debug,
    )

    # Register all API routers
    register_routers(app)

    return app
