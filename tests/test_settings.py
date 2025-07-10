import os
import tempfile

import pytest
import yaml

from app import settings as settings_module
from app.settings import Settings


# Mock get_resource_path to avoid depending on external file resolution
@pytest.fixture
def mock_get_resource_path(monkeypatch):
    monkeypatch.setattr("app.settings.get_resource_path", lambda path: path)


@pytest.fixture
def temp_config_file():
    config_data = {
        "ib": {"host": "testhost", "port": 4001, "client_id": 42},
        "logging": {"level": "DEBUG"},
        "fastapi": {"title": "Test App", "debug": True},
    }

    with tempfile.NamedTemporaryFile("w+", suffix=".yml", delete=False) as tmp:
        yaml.dump(config_data, tmp)
        tmp.flush()
        yield tmp.name

    os.remove(tmp.name)


def test_settings_load_success(mock_get_resource_path, temp_config_file):
    settings = Settings(config_path=temp_config_file)

    assert isinstance(settings.config, dict)
    assert "ib" in settings
    assert "fastapi" in settings
    assert settings["ib"]["host"] == "testhost"
    assert settings.get("logging")["level"] == "DEBUG"
    assert settings["fastapi"]["debug"] is True


def test_settings_missing_file_raises(mock_get_resource_path):
    with pytest.raises(FileNotFoundError):
        Settings(config_path="non_existent_file.yml")


def test_settings_dict_style_access(mock_get_resource_path, temp_config_file):
    settings = Settings(config_path=temp_config_file)
    assert settings["ib"]["client_id"] == 42
    assert "ib" in settings
    assert "fastapi" in settings


def test_settings_get_with_default(mock_get_resource_path, temp_config_file):
    settings = Settings(config_path=temp_config_file)
    assert settings.get("nonexistent", "default-value") == "default-value"


def test_settings_repr(mock_get_resource_path, temp_config_file):
    settings = Settings(config_path=temp_config_file)
    assert "Settings(" in repr(settings)


def test_get_settings_singleton(monkeypatch, mock_get_resource_path, temp_config_file):
    monkeypatch.setattr(settings_module, "_settings_instance", None)

    s1 = settings_module.get_settings(config_path=temp_config_file)
    s2 = settings_module.get_settings()

    assert s1 is s2
    assert s1["ib"]["port"] == 4001
