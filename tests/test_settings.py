import os
import tempfile
from pathlib import Path

import pytest

from app.settings import AppSettings, _load_config_yaml, get_settings

# Sample config for testing
SAMPLE_YAML = """
ib:
  host: test-host
  port: 1234

logging:
  level: WARNING

fastapi:
  title: Test API
  description: Test Description
  version: "1.0"
  docs_url: /test-docs
  redoc_url: /test-redoc
  openapi_url: /test-openapi.json
  debug: true

uvicorn:
  host: 127.0.0.1
  port: 8000
"""


@pytest.fixture
def temp_config_file():
    """Create a temporary YAML config file."""
    with tempfile.NamedTemporaryFile(mode="w+", suffix=".yml", delete=False) as tmp:
        tmp.write(SAMPLE_YAML)
        tmp_path = tmp.name
    yield tmp_path
    os.remove(tmp_path)


def test_load_config_yaml_success(temp_config_file):
    config = _load_config_yaml(temp_config_file)
    assert isinstance(config, dict)
    assert config["ib"]["host"] == "test-host"
    assert config["fastapi"]["debug"] is True


def test_load_config_yaml_file_not_found():
    with pytest.raises(FileNotFoundError):
        _load_config_yaml("non_existent_config.yml")


def test_get_settings_loads_correct_values(temp_config_file, monkeypatch):
    # Clear lru_cache
    get_settings.cache_clear()

    # Patch get_resource_path to return the actual path directly
    monkeypatch.setattr("app.settings.get_resource_path", lambda p: Path(p))

    settings = get_settings(config_path=temp_config_file)
    assert isinstance(settings, AppSettings)
    assert settings.ib.host == "test-host"
    assert settings.ib.port == 1234
    assert settings.fastapi.title == "Test API"
    assert settings.logging.level == "WARNING"


def test_get_settings_is_cached(temp_config_file, monkeypatch):
    get_settings.cache_clear()
    monkeypatch.setattr("app.settings.get_resource_path", lambda p: Path(p))

    settings_1 = get_settings(config_path=temp_config_file)
    settings_2 = get_settings(config_path=temp_config_file)
    assert settings_1 is settings_2
