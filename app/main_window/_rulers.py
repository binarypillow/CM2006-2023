from PyQt6 import QtWidgets, QtGui, QtCore
import numpy as np
import vtk
import random
from app.utils import get_abs_path


def on_left_button_press(self, obj, event, color):
    """Handles the left button press event to perform picking and draw rulers between selected cells."""

    # Get the position of the mouse click event
    click_pos = self.interactor.GetEventPosition()

    # Perform the pick operation
    self.cell_picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)

    # Get the picked cell
    picked_cell = self.cell_picker.GetCellId()

    # Get the picked actor
    picked_actor = self.cell_picker.GetActor()

    # Check if the picked actor is text
    if isinstance(picked_actor, vtk.vtkVectorText):
        return

    if picked_cell != -1:
        # Get the position of the picked cell
        picked_position = self.cell_picker.GetPickPosition()

        # Store the position of the picked cell
        self.selected_cell_positions.append(picked_position)

        # Create a sphere source at the picked position
        sphere = vtk.vtkSphereSource()
        sphere.SetCenter(picked_position)
        sphere.SetRadius(2)  # Set the radius of the sphere

        # Create a mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        # Create an actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(color)

        # Add the actor to the renderer
        self.renderer.AddActor(actor)
        self.selected_cells.append(actor)

        # If two cells have been selected, calculate the distance between them and draw a dotted line
        if len(self.selected_cell_positions) % 2 == 0:
            distance = np.linalg.norm(
                np.array(self.selected_cell_positions[-2])
                - np.array(self.selected_cell_positions[-1])
            )

            # Create a line source
            line_source = vtk.vtkLineSource()
            line_source.SetPoint1(self.selected_cell_positions[-2])
            line_source.SetPoint2(self.selected_cell_positions[-1])

            # Create a mapper
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputConnection(line_source.GetOutputPort())

            # Create an actor
            actor = vtk.vtkActor()
            actor.SetMapper(mapper)

            # Set the line style to dotted
            actor.GetProperty().SetLineStipplePattern(0x00FF)
            actor.GetProperty().SetLineStippleRepeatFactor(5)
            actor.GetProperty().SetColor(color)

            # Add the actor to the renderer
            self.renderer.AddActor(actor)
            self.line_btw_cells.append(actor)

            # Remove observer
            self.interactor.RemoveObserver(self.left_button_observer_id)
            # Restore cursor shape
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))

            # Enable focus once the ruler is created
            self.ui.glass_button.setDisabled(False)
            self.add_item_with_buttons(
                len(self.selected_cell_positions) // 2, distance, color
            )
            self.newruler_state = False
            self.ui.newruler_button.setText("Add ruler")

        # Render the scene
        self.vtk_widget.GetRenderWindow().Render()

    # Forward the event
    self.interactor.InvokeEvent("LeftButtonPressEvent")


def activate_left_click_event(self):
    """Activates or deactivates the left click event for adding rulers between cells."""

    # if the state is True (active), delete the progresses and cancel the operation
    if self.newruler_state:
        self.ui.glass_button.setDisabled(False)
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
        if len(self.selected_cell_positions) % 2 != 0:
            self.renderer.RemoveActor(self.selected_cells[-1])
            self.renderer.RemoveActor(self.selected_cells[-1])
            del self.selected_cells[-1]
            del self.selected_cell_positions[-1]
        self.interactor.RemoveObserver(self.left_button_observer_id)
        self.newruler_state = False
        self.ui.newruler_button.setText("Add ruler")
    else:  # if the state is False (not active), activate the functionality
        # Change the cursor shape
        self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
        # Create a random color for the ruler
        color = (random.random(), random.random(), random.random())
        # Create an observer for the left click events
        self.left_button_observer_id = self.interactor.AddObserver(
            "LeftButtonPressEvent",
            lambda obj, event: self.on_left_button_press(obj, event, color),
        )
        self.ui.glass_button.setDisabled(True)
        # Set the state as active = True
        self.newruler_state = True
        # Change the button name
        self.ui.newruler_button.setText("Cancel")


def add_item_with_buttons(self, text, dist, color):
    """Adds an item with buttons to the rulers' list."""

    item = QtWidgets.QListWidgetItem(f"ruler #{text}")
    self.ui.rulers_list.addItem(item)
    self.ui.rulers_list.setAlternatingRowColors(True)
    # Item state: Visible = False, Hidden = True
    self.item_states[f"ruler #{text}"] = False

    delete_button = QtWidgets.QPushButton()
    delete_button.setIcon(
        QtGui.QIcon(get_abs_path("/resources/icons/interface/trash.svg"))
    )  # Set the icon
    delete_button.setStyleSheet("background-color: transparent")
    delete_button.clicked.connect(lambda: self.delete_item(item))

    hide_button = QtWidgets.QPushButton()
    hide_button.setIcon(
        QtGui.QIcon(get_abs_path("/resources/icons/interface/eye.svg"))
    )  # Set the icon
    hide_button.setStyleSheet("background-color: transparent")
    hide_button.clicked.connect(lambda: self.hide_item(item, hide_button))

    color_button = (
        QtWidgets.QPushButton()
    )  # Create a new QPushButton to store the ruler's color
    color_button.setStyleSheet(
        f"background-color: rgb{tuple(int(c * 255) for c in color)}; border-radius: 4px;"
    )
    color_button.setMaximumSize(10, 10)  # Set the maximum width and height

    # Add the measurement's value in a label
    label = QtWidgets.QLabel(f"{dist:.2f} mm")

    # Build the item
    widget = QtWidgets.QWidget()
    layout = QtWidgets.QHBoxLayout(widget)
    layout.addWidget(label)
    layout.addWidget(color_button)
    layout.addSpacing(5)
    layout.addWidget(hide_button)
    layout.addWidget(delete_button)
    layout.setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
    layout.setContentsMargins(0, 0, 0, 0)
    widget.setLayout(layout)

    # Add the item to the list
    self.ui.rulers_list.setItemWidget(item, widget)


def delete_item(self, item):
    """Deletes an item from the rulers list and removes the corresponding actors and positions."""

    row = self.ui.rulers_list.row(item)
    self.ui.rulers_list.takeItem(row)
    # Delete the corresponding actors, positions and the line connecting them.
    self.renderer.RemoveActor(self.selected_cells[row * 2])
    self.renderer.RemoveActor(self.selected_cells[row * 2 + 1])
    self.renderer.RemoveActor(self.line_btw_cells[row])
    del self.line_btw_cells[row]
    del self.selected_cells[row * 2 : row * 2 + 2]
    del self.selected_cell_positions[row * 2 : row * 2 + 2]

    # Refresh the scene
    self.vtk_widget.GetRenderWindow().Render()

    # Update the list and resort the items
    for i in range(row, self.ui.rulers_list.count()):
        item = self.ui.rulers_list.item(i)
        item.setText(f"ruler #{i+1}")
        self.item_states[f"ruler #{i+1}"] = self.item_states[f"ruler #{i+2}"]
    self.item_states.popitem()


def hide_item(self, item, button):
    """Toggles the visibility of an item in the rulers list and updates the corresponding actors in the scene."""

    row = self.ui.rulers_list.row(item)
    # Check the state of the item and set the icon accordingly
    if self.item_states[item.text()]:
        button.setIcon(QtGui.QIcon(get_abs_path("/resources/icons/interface/eye.svg")))
        self.renderer.AddActor(self.selected_cells[row * 2])
        self.renderer.AddActor(self.selected_cells[row * 2 + 1])
        self.renderer.AddActor(self.line_btw_cells[row])
    else:
        button.setIcon(
            QtGui.QIcon(get_abs_path("/resources/icons/interface/eye-slash.svg"))
        )
        self.renderer.RemoveActor(self.selected_cells[row * 2])
        self.renderer.RemoveActor(self.selected_cells[row * 2 + 1])
        self.renderer.RemoveActor(self.line_btw_cells[row])

    # Refresh the scene
    self.vtk_widget.GetRenderWindow().Render()

    # Toggle the state of the item
    self.item_states[item.text()] = not self.item_states[item.text()]
