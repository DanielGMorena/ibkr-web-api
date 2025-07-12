import uvicorn

from app.app_factory import create_app
from app.cli_args import parse_args
from app.settings import get_settings

args = parse_args()
settings = get_settings(args.config)
app = create_app()


if __name__ == "__main__":
    uvicorn.run(app, host=settings.uvicorn.host, port=settings.uvicorn.port)
