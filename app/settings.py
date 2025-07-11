import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional, Union

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from app.utils.files import get_resource_path

# Load environment variables from a .env file if present
load_dotenv()


def _load_config_yaml(file_path: Union[Path, str]) -> Any:
    """
    Load and parse a YAML configuration file.

    Args:
        file_path (Union[Path, str]): Path to the YAML config file.

    Returns:
        dict: Parsed YAML configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
        yaml.YAMLError: If the YAML is invalid.
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path

    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path.resolve()}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


class _IBSettings(BaseSettings):
    """Settings for the IBKR connection."""

    host: str
    port: int


class _LoggingSettings(BaseSettings):
    """Logging configuration settings."""

    level: str = "INFO"


class _FastAPISettings(BaseSettings):
    """Settings for FastAPI app configuration."""

    title: str
    description: str
    version: str
    docs_url: Optional[str] = "/docs"
    redoc_url: Optional[str] = "/redoc"
    openapi_url: Optional[str] = "/openapi.json"
    debug: bool = False


class _UvicornSettings(BaseSettings):
    """Settings for Uvicorn server configuration."""

    host: str = "127.0.0.1"
    port: int = 8000


class AppSettings(BaseSettings):
    """
    Application-wide settings object.

    Aggregates configuration sections for various subsystems.
    """

    ib: _IBSettings
    logging: _LoggingSettings
    fastapi: _FastAPISettings
    uvicorn: _UvicornSettings

    model_config = {
        "env_prefix": "",
        "env_nested_delimiter": "__",
    }


@lru_cache()
def get_settings(config_path: Optional[str] = None) -> AppSettings:
    """
    Load and return a singleton instance of AppSettings.
    """
    raw_path: Optional[str] = config_path or os.getenv("APP_CONFIG", "app/config.yml")

    if raw_path is None:
        raise ValueError("No config path provided and APP_CONFIG is not set")

    resolved_path: str = raw_path  # Now it's guaranteed to be str
    resource_path = get_resource_path(resolved_path)
    config_dict = _load_config_yaml(resource_path)
    return AppSettings(**config_dict)
