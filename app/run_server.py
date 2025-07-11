import uvicorn

from app.app_factory import create_app
from app.settings import get_settings

settings = get_settings()
app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.uvicorn.host, port=settings.uvicorn.port)
