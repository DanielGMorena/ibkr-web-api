import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

from app.utils import get_resource_path


class Settings:
    """
    Application configuration loader.

    Loads settings from a YAML file and exposes them as typed attributes.

    Attributes:
        IB_HOST (str): Host for IBKR TWS or Gateway.
        IB_PORT (int): Port number for the IBKR API.
        IB_CLIENT_ID (int): Client ID for the IB API session.
        LOG_LEVEL (str): Logging level (e.g., "DEBUG", "INFO").
    """

    def __init__(self, config_path: str = None):
        """
        Initialize the settings from a YAML config file.

        Args:
            config_path (str, optional): Path to the YAML config file.
                Defaults to 'config.yml' or the path set in the APP_CONFIG environment variable.
        """
        load_dotenv()
        config_file = config_path or os.environ.get("APP_CONFIG", "config.yml")
        resolved_path = get_resource_path(config_file)
        self._config: Dict[str, Any] = self._load_yaml(resolved_path)
        self._parse()

    def _load_yaml(self, path: str) -> Dict[str, Any]:
        """
        Load YAML file.

        Args:
            path (str): Path to the YAML file.

        Returns:
            dict: Parsed YAML data.
        """
        full_path = Path(path)
        if not full_path.exists():
            raise FileNotFoundError(f"Config file not found: {full_path.resolve()}")
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def _parse(self) -> None:
        """Parse and assign config values to attributes with type enforcement."""
        ib = self._config.get("ib", {})
        logging_cfg = self._config.get("logging", {})

        self.IB_HOST: str = str(ib.get("host", "127.0.0.1"))
        self.IB_PORT: int = int(ib.get("port", 7497))
        self.IB_CLIENT_ID: int = int(ib.get("client_id", 1))
        self.LOG_LEVEL: str = str(logging_cfg.get("level", "INFO")).upper()


# Lazy-loaded singleton instance
_settings_instance: Optional[Settings] = None


def get_settings(config_path: Optional[str] = None) -> Settings:
    """
    Get the global settings instance (singleton), loading from config if not already initialized.

    Args:
        config_path (Optional[str]): Optional path to the configuration file.

    Returns:
        Settings: The loaded settings instance.
    """
    global _settings_instance
    if _settings_instance is None:
        _settings_instance = Settings(config_path)
    return _settings_instance
