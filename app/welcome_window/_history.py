import yaml
import os


def save_history(self):
    """Save the current state into a YAML file."""
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
    """Load the history from a YAML file and update the UI with the saved paths."""
    if not os.path.exists(self.history_path):
        return False
    try:
        with open(self.history_path, "r") as f:
            history = yaml.safe_load(f)
            self.ui.img_text.setText(history["img_path"])
            self.img_path = history["img_path"]
            self.ui.seg_text.setText(history["seg_path"])
            self.seg_path = history["seg_path"]
        self.ui.img_button.setChecked(True)
        self.ui.seg_button.setChecked(True)
        return history
    except Exception:
        return False
