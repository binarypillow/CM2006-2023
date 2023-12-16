import os
import sys


def get_root_dir():
    """
    Returns the root directory of the application.

    Returns:
        str: The absolute path of the root directory.
    """
    return getattr(
        sys, "_MEIPASS", os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    )


def get_abs_path(rel_path=""):
    """
    Returns the absolute path by joining the root directory with the given relative path.

    Args:
        rel_path (str): The relative path to be joined with the root directory. Defaults to an empty string.

    Returns:
        str: The absolute path obtained by joining the root directory and the relative path.
    """
    root = get_root_dir()
    return os.path.join(root, f"app/{rel_path}")
