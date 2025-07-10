import logging
import os
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv

from app.utils import get_resource_path

logger = logging.getLogger(__name__)


class Settings:
    """
    Application configuration loader.

    Loads all settings into a single flat dictionary for flexible access.
    """

    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the settings from a YAML config file.

        Args:
            config_path (Optional[str]): Path to the YAML config file.
                Defaults to 'config.yml' or the path set in the APP_CONFIG environment variable.
        """
        load_dotenv()
        config_file = config_path or os.environ.get("APP_CONFIG", "config.yml")
        resolved_path = get_resource_path(config_file)
        logger.info(f"Loading settings from config file: {resolved_path}")
        self.config: Dict[str, Any] = self._load_yaml(resolved_path)

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
            logger.error(f"Config file not found: {full_path.resolve()}")
            raise FileNotFoundError(f"Config file not found: {full_path.resolve()}")

        logger.debug(f"Reading config YAML: {full_path.resolve()}")
        with open(full_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retrieve a top-level config value by key.

        Args:
            key (str): The top-level key to retrieve.
            default (Any): Default value if key is not found.

        Returns:
            Any: The value from the config dictionary.
        """
        return self.config.get(key, default)

    def __getitem__(self, key: str) -> Any:
        """Allows dict-style access: settings['ib']"""
        return self.config[key]

    def __contains__(self, key: str) -> bool:
        """Allow `in` checks like 'ib' in settings"""
        return key in self.config

    def __repr__(self) -> str:
        return f"Settings({self.config})"


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
