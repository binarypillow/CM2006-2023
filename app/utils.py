import os
import sys
import yaml


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


def get_keys_from_yaml(file_path):
    """
    Retrieves the keys (organs' name) from a YAML file.

    Args:
        file_path (str): The path to the YAML file.

    Returns:
        list: A list of keys extracted from the YAML file.
    """
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return list(data.keys())


def get_index_from_key(key, file_path):
    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data[key]
