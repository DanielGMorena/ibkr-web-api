import sys
from pathlib import Path
from typing import Union


def get_resource_path(relative_path: Union[str, Path]) -> Path:
    """
    Get absolute path to a resource, compatible with PyInstaller bundles and dev mode.

    Args:
        relative_path (Union[str, Path]): Path relative to the script or bundled root.

    Returns:
        Path: Absolute path to the resource.
    """
    if getattr(sys, "frozen", False):
        # Running in a PyInstaller bundle
        base_path = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        # Running in a normal Python environment
        base_path = Path.cwd()

    return base_path / Path(relative_path)
