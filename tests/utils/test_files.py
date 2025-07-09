import sys
from pathlib import Path

from app.utils import get_resource_path


def test_get_resource_path_dev_mode():
    """Test resource path in development mode."""
    relative_path = "config.yml"
    result = get_resource_path(relative_path)

    # Check that the path ends with the relative part
    assert result.name == "config.yml"

    # Check that it's a Path object and joined properly
    assert isinstance(result, Path)
    assert relative_path in str(result)


def test_get_resource_path_frozen_mode(monkeypatch, tmp_path):
    """Test resource path in frozen (PyInstaller) mode."""
    # Patch sys module attributes
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    object.__setattr__(
        sys, "_MEIPASS", str(tmp_path)
    )  # Force set the hidden attr manually

    relative_path = "assets/sample.txt"
    expected = tmp_path / relative_path
    result = get_resource_path(relative_path)

    assert result == expected
