from PyQt6 import QtWidgets


def get_checked_labels(self):
    """Retrieves the checked labels from the labels' list."""
    checked_labels = []
    scroll_layout = self.ui.labels_list.widget().layout()
    for i in range(scroll_layout.count()):
        widget = scroll_layout.itemAt(i).widget()
        if isinstance(widget, QtWidgets.QCheckBox) and widget.isChecked():
            checked_labels.append(widget.text())
    return checked_labels
