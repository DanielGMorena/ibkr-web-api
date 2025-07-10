from fastapi import FastAPI

from app.api.hist_mkt_data import router as hist_mkt_data_router


def register_routers(app: FastAPI) -> None:
    """
    Register all API routers with the FastAPI application.

    This function includes the routers defined across the application
    modules (e.g., hist_mkt_data) into the main FastAPI app instance.

    Args:
        app (FastAPI): The FastAPI application to register routes on.
    """
    app.include_router(hist_mkt_data_router)
