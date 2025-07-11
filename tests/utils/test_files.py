import sys
from pathlib import Path

from app.utils import get_resource_path


def test_get_resource_path_dev_mode_str():
    """Test resource path in development mode with str input."""
    relative_path = "config.yml"
    result = get_resource_path(relative_path)

    assert isinstance(result, Path)
    assert result.name == "config.yml"
    assert relative_path in str(result)


def test_get_resource_path_dev_mode_path():
    """Test resource path in development mode with Path input."""
    relative_path = Path("config.yml")
    result = get_resource_path(relative_path)

    assert isinstance(result, Path)
    assert result.name == "config.yml"
    assert "config.yml" in str(result)


def test_get_resource_path_frozen_mode_str(monkeypatch, tmp_path):
    """Test resource path in frozen (PyInstaller) mode with str input."""
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    object.__setattr__(sys, "_MEIPASS", str(tmp_path))

    relative_path = "assets/sample.txt"
    expected = tmp_path / relative_path
    result = get_resource_path(relative_path)

    assert result == expected


def test_get_resource_path_frozen_mode_path(monkeypatch, tmp_path):
    """Test resource path in frozen (PyInstaller) mode with Path input."""
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    object.__setattr__(sys, "_MEIPASS", str(tmp_path))

    relative_path = Path("assets/sample.txt")
    expected = tmp_path / relative_path
    result = get_resource_path(relative_path)

    assert result == expected
