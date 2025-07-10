from fastapi import FastAPI

from app.api import register_routers


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    This function initializes the FastAPI app, registers all routers,
    and returns the app instance for use by an ASGI server like Uvicorn.

    Returns:
        FastAPI: A configured FastAPI application instance.
    """
    app = FastAPI()
    register_routers(app)
    return app


app = create_app()
