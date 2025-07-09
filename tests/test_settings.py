from pathlib import Path

import pytest

from app.settings import Settings, get_settings


@pytest.fixture
def sample_config(tmp_path) -> Path:
    """Creates a temporary config.yml file for testing."""
    config_path = tmp_path / "config.yml"
    config_path.write_text(
        """
        ib:
          host: "192.168.1.10"
          port: 4002
          client_id: 42
        logging:
          level: "debug"
        """,
        encoding="utf-8",
    )
    return config_path


@pytest.fixture(autouse=True)
def reset_settings_instance(monkeypatch):
    """Ensure _settings_instance is reset between tests."""
    monkeypatch.setattr("app.settings._settings_instance", None)


def test_settings_parses_yaml_correctly(sample_config):
    """Test that settings are parsed correctly from a valid config file."""
    settings = Settings(str(sample_config))

    assert settings.IB_HOST == "192.168.1.10"
    assert settings.IB_PORT == 4002
    assert settings.IB_CLIENT_ID == 42
    assert settings.LOG_LEVEL == "DEBUG"  # should be uppercased


def test_get_settings_returns_singleton(sample_config):
    """Test that get_settings returns the same instance every time."""
    first = get_settings(str(sample_config))
    second = get_settings()

    assert first is second


def test_missing_config_file_raises(tmp_path):
    """Test that missing config file raises FileNotFoundError."""
    missing_path = tmp_path / "nonexistent.yml"

    with pytest.raises(FileNotFoundError):
        Settings(str(missing_path))


def test_settings_uses_default_values(tmp_path):
    """Test fallback/default values when fields are missing in config."""
    config_path = tmp_path / "minimal_config.yml"
    config_path.write_text(
        """
        ib: {}
        logging: {}
        """,
        encoding="utf-8",
    )

    settings = Settings(str(config_path))

    assert settings.IB_HOST == "127.0.0.1"
    assert settings.IB_PORT == 7497
    assert settings.IB_CLIENT_ID == 1
    assert settings.LOG_LEVEL == "INFO"
