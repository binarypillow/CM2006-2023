from PyQt6 import QtWidgets


def get_checked_labels(self):
    """
    Returns a list of checked labels.

    Args:
        self: The instance of the class.

    Returns:
        list: A list of the checked labels.
    """

    checked_labels = []
    scroll_layout = self.ui.labels_list.widget().layout()
    for i in range(scroll_layout.count()):
        widget = scroll_layout.itemAt(i).widget()
        if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
            checked_labels.append(widget.text())
    return checked_labels
