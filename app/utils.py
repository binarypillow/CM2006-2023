import os
import sys
import yaml
import numpy as np


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
        rel_path (str): The relative path to be joined with the root directory. Default to an empty string.

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
    """
    Retrieves the value associated with the given key from a YAML file.

    Args:
        key (str): The key to search for in the YAML file.
        file_path (str): The path to the YAML file.

    Returns:
        Any: The value associated with the given key.
    """

    with open(file_path, "r") as file:
        data = yaml.safe_load(file)
    return data[key]


def convert_to_gray_scale(hu_values):
    """
    Converts Hounsfield Unit (HU) values to grayscale values.

    Args:
        hu_values (np.ndarray): Array of HU values.

    Returns:
        np.ndarray: Array of grayscale values.
    """

    hu_values = np.array(hu_values)
    gray_scale_values = np.zeros(hu_values.shape, dtype=np.uint8)

    mask = hu_values < -100
    gray_scale_values[mask] = 0

    mask = (hu_values >= -100) & (hu_values <= 100)
    gray_scale_values[mask] = ((hu_values[mask] + 100) / 200) * 127

    mask = (hu_values > 100) & (hu_values <= 3000)
    gray_scale_values[mask] = ((hu_values[mask] - 100) / 2900) * 128 + 127

    mask = hu_values > 3000
    gray_scale_values[mask] = 255

    return gray_scale_values
