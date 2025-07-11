# main.py

from .app_factory import create_app

# Create the FastAPI app instance using the application factory.
# This instance will be discovered by ASGI servers like Uvicorn.
app = create_app()
