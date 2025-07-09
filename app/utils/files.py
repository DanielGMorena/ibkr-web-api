import sys
from pathlib import Path


def get_resource_path(relative_path: str) -> Path:
    """
    Get absolute path to a resource, compatible with PyInstaller bundles and dev mode.

    Args:
        relative_path (str): Path relative to the script or bundled root.

    Returns:
        Path: Absolute path to the resource.
    """
    if getattr(sys, "frozen", False):
        # Running in a PyInstaller bundle
        base_path = Path(sys._MEIPASS)
    else:
        # Running in a normal Python environment
        base_path = Path(__file__).resolve().parent.parent  # adjust as needed
    return base_path / relative_path
