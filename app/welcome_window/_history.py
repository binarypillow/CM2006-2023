import yaml
import os


def save_history(self):
    """
    Saves the history of selected files and checked labels to a YAML file.

    Args:
        self: The instance of the class.

    Returns:
        None
    """

    with open(self.history_path, "w") as f:
        yaml.dump(
            {
                "img_path": self.img_path,
                "seg_path": self.seg_path,
                "checked_labels": self.get_checked_labels(),
            },
            f,
        )


def load_history(self):
    """
    Loads the history of selected files from a YAML file and updates the corresponding UI elements.

    Args:
        self: The instance of the class.

    Returns:
        dict or bool: The loaded history as a dictionary if successful, False otherwise.
    """

    if not os.path.exists(self.history_path):
        return False
    try:
        with open(self.history_path, "r") as f:
            history = yaml.safe_load(f)
            # Set the values read in the YAML file
            self.ui.img_text.setText(history["img_path"])
            self.img_path = history["img_path"]
            self.ui.seg_text.setText(history["seg_path"])
            self.seg_path = history["seg_path"]
        self.ui.img_button.setChecked(True)
        self.ui.seg_button.setChecked(True)

        return history

    except IOError as e:
        print(f"Error opening file: {e}")
        return False
