import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

# Load environment variables from a .env file if present
load_dotenv()


def _load_config_yaml(file_path: str) -> Dict[str, Any]:
    """
    Load and parse a YAML configuration file.

    Args:
        file_path (str): Path to the YAML config file.

    Returns:
        dict: Parsed YAML configuration as a dictionary.

    Raises:
        FileNotFoundError: If the file does not exist.
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path.resolve()}")

    with open(path, "r", encoding="utf-8") as f:
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

    host: Optional[str] = "127.0.0.1"
    port: Optional[int] = 8000


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

    Args:
        config_path (Optional[str]): Optional path to a YAML config file.
            Defaults to the value in APP_CONFIG env var, or 'config.yml'.

    Returns:
        AppSettings: The application's settings object.
    """
    resolved_path = config_path or os.getenv("APP_CONFIG", "app/config.yml")
    config_dict = _load_config_yaml(resolved_path)
    return AppSettings(**config_dict)
