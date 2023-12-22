from PyQt6 import QtWidgets, QtGui, QtCore
from PyQt6.QtWidgets import QColorDialog
from matplotlib.figure import Figure
import matplotlib.patches as patches
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import numpy as np
import vtk
import random
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import nibabel as nib
from vtkmodules.util.numpy_support import numpy_to_vtk
from app.stereo_dialog import StereoParam
from app.about_dialog import AboutText
from app.ui import main_interface
from app.utils import get_index_from_key, get_abs_path, convert_to_gray_scale
from app.callback import TimerCallback


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, path_img, path_label, checked_labels):
        self.checked_labels = checked_labels
        # Load the nii.gz file with the images
        self.img_nii = nib.load(path_img)
        self.img_data = self.img_nii.get_fdata()

        # Load the nii.gz file with the labels
        labels_nii = nib.load(path_label)
        self.labels_data = labels_nii.get_fdata()

        # Create a list containing each organ separated
        (
            self.segmented_organs_data,
            self.segmented_organs,
        ) = self.createListSegmentedOrgans()

        # Colors for surface organs
        self.colors = [
            (0.86, 0.37, 0.34),  # Red
            (0.48, 0.77, 0.46),  # Green
            (0.32, 0.58, 0.89),  # Blue
            (0.77, 0.57, 0.44),  # Brown
            (0.73, 0.6, 0.86),  # Purple
            (0.35, 0.7, 0.67),  # Cyan
            (0.96, 0.78, 0.25),  # Yellow
            (0.89, 0.48, 0.74),  # Pink
            (0.56, 0.82, 0.87),  # Turquoise
            (0.62, 0.62, 0.62),  # Gray
            (0.97, 0.51, 0.47),  # Coral
            (0.65, 0.85, 0.33),  # Lime
            (1.0, 0.81, 0.37),  # Gold
        ]

        super(MainWindow, self).__init__()
        self.ui = main_interface.Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle("Visualization application")
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.render_frame)
        self.ui.vtk_frame.addWidget(self.vtk_widget)

        # Create a list of volume actors: each element in the list is an actor for one organ
        self.segmented_volume_actors = self.createSegmentedVolumeActors()

        # Create a list of surface actors: each element in the list is an actor for one organ
        self.segmented_surface_actors = self.createSegmentedSurfaceActors()

        # Default rendering: surface
        # self.segmented_actors defines the displayed actors
        self.segmented_actors = list(self.segmented_surface_actors)

        # Create a VTK renderer
        self.renderer = vtk.vtkRenderer()

        # Add the actors to the renderer and set the background color
        for actor in self.segmented_actors:
            self.renderer.AddActor(actor)
        self.renderer.SetBackground(1, 1, 1)  # White background

        # Add the renderer to the window
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)

        # Initialize stereo rendering
        self.vtk_widget.GetRenderWindow().GetStereoCapableWindow()
        self.vtk_widget.GetRenderWindow().StereoCapableWindowOn()

        # Set up the camera and start the interactor
        self.renderer.ResetCamera()

        # Initial position of the camera
        self.renderer.GetActiveCamera().SetPosition(-0.68699, -371.3468, 61.26843)
        self.renderer.GetActiveCamera().Roll(110)

        # Set interactor, initialize and start
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()

        # Create a cell picker
        self.cell_picker = vtk.vtkCellPicker()
        # Set the tolerance for picking a point
        self.cell_picker.SetTolerance(0.0005)

        self.interactor.Start()

        self.default_focal = self.renderer.GetActiveCamera().GetFocalPoint()

        # Window for about dialog
        self.about_window = AboutText()

        ##############################################################################################
        # MENU TOOLS BAR

        # About menu button
        self.ui.actionInfo.triggered.connect(self.onAboutClicked)

        # Exit menu button
        self.ui.actionClose.triggered.connect(self.close)

        ##############################################################################################
        # INTERACTIONS AND BUTTONS

        # Initialize color
        self.ui.color_button.setStyleSheet(
            f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in self.colors[0])}"
        )

        # Create a cell picker
        self.cell_picker = vtk.vtkCellPicker()
        # Set the tolerance for picking a point
        self.cell_picker.SetTolerance(0.0005)

        # Know the position of the camera each right-click: just for us, to better place the camera
        self.interactor.AddObserver("RightButtonPressEvent", self.get_camera_position)

        self.current_ipd = self.renderer.GetActiveCamera().GetEyeAngle()
        # Window for stereo parameters
        self.stereo_window = StereoParam(self.current_ipd)

        # Change the actor from surface to volume if the volume button is checked
        self.ui.volume_button.setChecked(False)  # initial state : unchecked
        self.ui.volume_button.clicked.connect(self.onVolumeButtonClicked)

        # Slide for opacity change
        self.ui.op_slider.valueChanged.connect(self.onOpacityChanged)

        # Create the slider list
        for organ in self.checked_labels:
            self.ui.organ_combo.addItem(organ)

        # Change the view and show volume rendering if the glass button is clicked
        self.ui.glass_button.clicked.connect(self.onGlassButtonClicked)
        self.ui.color_button.clicked.connect(self.onColorButtonClicked)

        # Change the organ view and volume rendering if user changes the specified organ
        self.ui.organ_combo.currentIndexChanged.connect(self.onComboBoxChanged)

        # Display stereo if clicked. Display a parameter button to adjust stereo parameters
        self.ui.stereo_button.clicked.connect(self.onStereoClicked)

        # Choose stereo parameters. It opens a new dialog window
        self.ui.stereo_param_button.clicked.connect(self.onStereoParamClicked)

        self.ui.actionClose.triggered.connect(self.close)

        histogram_canvas = self.create_histogram(self.segmented_organs_data)
        self.ui.hist_layout.addWidget(histogram_canvas)

        self.ui.low_slider.valueChanged.connect(self.onSliderChanged)
        self.ui.high_slider.valueChanged.connect(self.onSliderChanged)
        self.ui.high_op_slider.valueChanged.connect(self.onSliderChanged)

        self.ui.update_button.clicked.connect(self.onVolumeUpdate)

        # Create a button
        self.ui.newruler_button.clicked.connect(self.activate_left_click_event)

        self.newruler_state = False

        self.selected_cells = []
        self.selected_cell_positions = []
        self.line_btw_cells = []

        self.left_button_observer_id = 0

        self.item_states = {}

        volume, surface = self.calculate_volume_surface()

        self.ui.volume_value.setText(f"{volume:,.2f} mm³")
        self.ui.surface_value.setText(f"{surface:,.2f} mm²")

    def add_item_with_delete_button(self, text, dist, color):
        item = QtWidgets.QListWidgetItem(f"ruler #{text}")
        self.ui.rulers_list.addItem(item)
        self.ui.rulers_list.setAlternatingRowColors(True)
        self.item_states[f"ruler #{text}"] = False

        delete_button = QtWidgets.QPushButton()
        delete_button.setIcon(
            QtGui.QIcon(get_abs_path("resources/icons/interface/trash.svg"))
        )  # Set the icon
        delete_button.setStyleSheet("background-color: transparent")
        delete_button.clicked.connect(lambda: self.delete_item(item))

        hide_button = QtWidgets.QPushButton()
        hide_button.setIcon(
            QtGui.QIcon(get_abs_path("resources/icons/interface/eye.svg"))
        )  # Set the icon
        hide_button.setStyleSheet("background-color: transparent")
        hide_button.clicked.connect(lambda: self.hide_item(item, hide_button))

        color_button = QtWidgets.QPushButton()  # Create a new QPushButton
        color_button.setStyleSheet(
            f"background-color: rgb{tuple(int(c * 255) for c in color)}; border-radius: 4px;"
        )
        color_button.setMaximumSize(10, 10)  # Set the maximum width and height

        label = QtWidgets.QLabel(f"{dist:.2f} mm")

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

        self.ui.rulers_list.setItemWidget(item, widget)

    def delete_item(self, item):
        row = self.ui.rulers_list.row(item)
        self.ui.rulers_list.takeItem(row)
        self.renderer.RemoveActor(self.selected_cells[row * 2])
        self.renderer.RemoveActor(self.selected_cells[row * 2 + 1])
        self.renderer.RemoveActor(self.line_btw_cells[row])
        del self.line_btw_cells[row]
        del self.selected_cells[row * 2 : row * 2 + 2]
        del self.selected_cell_positions[row * 2 : row * 2 + 2]

        # Render the scene
        self.vtk_widget.GetRenderWindow().Render()

        for i in range(row, self.ui.rulers_list.count()):
            item = self.ui.rulers_list.item(i)
            item.setText(f"ruler #{i+1}")
            self.item_states[f"ruler #{i+1}"] = self.item_states[f"ruler #{i+2}"]

        self.item_states.popitem()

    def hide_item(self, item, button):
        row = self.ui.rulers_list.row(item)
        # Check the state of the item and set the icon accordingly
        if self.item_states[item.text()]:
            button.setIcon(
                QtGui.QIcon(get_abs_path("resources/icons/interface/eye.svg"))
            )
            self.renderer.AddActor(self.selected_cells[row * 2])
            self.renderer.AddActor(self.selected_cells[row * 2 + 1])
            self.renderer.AddActor(self.line_btw_cells[row])
        else:
            button.setIcon(
                QtGui.QIcon(get_abs_path("resources/icons/interface/eye-slash.svg"))
            )
            self.renderer.RemoveActor(self.selected_cells[row * 2])
            self.renderer.RemoveActor(self.selected_cells[row * 2 + 1])
            self.renderer.RemoveActor(self.line_btw_cells[row])

        # Render the scene
        self.vtk_widget.GetRenderWindow().Render()

        # Toggle the state of the item
        self.item_states[item.text()] = not self.item_states[item.text()]

    def calculate_volume_surface(self):
        selected_index = self.ui.organ_combo.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        # Convert the actor's polydata to a closed surface
        surface_filter = vtk.vtkDataSetSurfaceFilter()
        surface_filter.SetInputData(selected_surface_actor.GetMapper().GetInput())
        surface_filter.Update()

        # Use vtkMassProperties to compute the volume
        mass_properties = vtk.vtkMassProperties()
        mass_properties.SetInputData(surface_filter.GetOutput())
        mass_properties.Update()

        return mass_properties.GetVolume(), mass_properties.GetSurfaceArea()

    def activate_left_click_event(self):
        if self.newruler_state:
            self.ui.glass_button.setDisabled(False)
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
            if len(self.selected_cell_positions) % 2 != 0:
                self.renderer.RemoveActor(self.selected_cells[-1])
                self.renderer.RemoveActor(self.selected_cells[-1])
                del self.selected_cells[-1]
                del self.selected_cell_positions[-1]
            print(len(self.selected_cell_positions))
            self.interactor.RemoveObserver(self.left_button_observer_id)
            self.newruler_state = False
            self.ui.newruler_button.setText("Add ruler")
        else:
            self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.PointingHandCursor))
            color = (random.random(), random.random(), random.random())
            self.left_button_observer_id = self.interactor.AddObserver(
                "LeftButtonPressEvent",
                lambda obj, event: self.on_left_button_press(obj, event, color),
            )
            self.ui.glass_button.setDisabled(True)
            self.newruler_state = True
            self.ui.newruler_button.setText("Cancel")

    def on_left_button_press(self, obj, event, color):
        # Get the position of the mouse click event
        click_pos = self.interactor.GetEventPosition()

        # Perform the pick operation
        self.cell_picker.Pick(click_pos[0], click_pos[1], 0, self.renderer)

        # Get the picked cell
        picked_cell = self.cell_picker.GetCellId()

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

                self.interactor.RemoveObserver(self.left_button_observer_id)
                self.setCursor(QtGui.QCursor(QtCore.Qt.CursorShape.ArrowCursor))
                self.ui.glass_button.setDisabled(False)
                self.add_item_with_delete_button(
                    len(self.selected_cell_positions) // 2, distance, color
                )
                self.newruler_state = False
                self.ui.newruler_button.setText("Add ruler")

            # Render the scene
            self.vtk_widget.GetRenderWindow().Render()

        # Forward the event
        self.interactor.InvokeEvent("LeftButtonPressEvent")

    def onVolumeUpdate(self):
        # Adjust opacity for a selected organ
        selected_index = self.ui.organ_combo.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        selected_volume_actor = self.segmented_volume_actors[selected_index]
        opacity = self.ui.op_slider.value() / 100

        # Set opacity for the surface actor
        selected_surface_actor.GetProperty().SetOpacity(opacity)

        # Set opacity for the surface actor
        selected_surface_actor.GetProperty().SetOpacity(opacity)

        # Set opacity for the volume actor
        opacity_func = vtk.vtkPiecewiseFunction()

        opacity_func.AddPoint(self.ui.low_slider.value(), 0)
        opacity_func.AddPoint(
            self.ui.high_slider.value(), self.ui.high_op_slider.value() / 100
        )
        selected_volume_actor.GetProperty().SetScalarOpacity(opacity_func)
        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onSliderChanged(self):
        # Remove the old histogram canvas
        while self.ui.hist_layout.count():
            child = self.ui.hist_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Create a new histogram canvas with the updated vertical line position
        new_histogram_canvas = self.create_histogram(self.segmented_organs_data)

        # Add the new histogram canvas to the layout
        self.ui.hist_layout.addWidget(new_histogram_canvas)

        # Set constraints to avoid an invalid or empty interval
        self.ui.low_slider.setMaximum(self.ui.high_slider.value() - 1)
        self.ui.high_slider.setMinimum(self.ui.low_slider.value() + 1)

    def create_histogram(self, organs_data):
        current_selected = self.ui.organ_combo.currentIndex()
        organ_data = convert_to_gray_scale(organs_data[current_selected])
        organ_data = organ_data[organ_data != 0]

        # Calculate the histogram data
        hist_data, bin_edges = np.histogram(organ_data, bins=256, range=(0, 256))

        # Create a FigureCanvas object
        canvas = FigureCanvas(Figure(figsize=(5, 3), dpi=100))

        ax = canvas.figure.subplots()
        # Create the histogram and get the bin values (counts)
        counts, bins, _ = ax.hist(
            hist_data,
            bins=128,
            range=[0, 256],
            density=False,
        )

        # Normalize the bin values
        counts_normalized = counts / np.sum(counts)

        # Clear the current figure
        ax.clear()

        # Plot the histogram with the normalized frequencies
        ax.bar(bins[:-1], counts_normalized, width=2, color="grey")

        # Define the coordinates of the four points of the polygon
        polygon_points = [
            (self.ui.low_slider.value(), 0),
            (self.ui.high_slider.value(), 0),
            (self.ui.high_slider.value(), self.ui.high_op_slider.value() / 100),
        ]
        # Create a Polygon object
        polygon = patches.Polygon(
            polygon_points,
            facecolor="lightgrey",
            alpha=0.5,
            linewidth=1.2,
            linestyle="--",
        )

        # Add the polygon to the current axes
        ax.add_patch(polygon)

        ax.set_ylim([0, 1])

        # Mark the vertices with gray dots
        for point in polygon_points:
            ax.scatter(*point, s=8, color="lightgrey", edgecolors="black")

        return canvas

    def get_camera_position(self, obj, event):
        """
        Retrieves the position and roll angle of the camera.

        This method is triggered by a right-click mouse event and prints the current position and roll angle of the
        camera. The camera position and roll angle can be used for making adjustments in focus mode.

        Args:
            obj: The object that triggered the event.
            event: The event that occurred.

        Returns:
            None
        """
        # Get the position of the camera at right click mouse to make adjustments for focus mode
        position = self.renderer.GetActiveCamera().GetPosition()
        angle = self.renderer.GetActiveCamera().GetRoll()
        print("Camera's position :", position)
        print("Camera's Roll :", angle)

    def onStereoParamClicked(self):
        """
        Handles the click event of the stereo parameter button.

        This method opens the stereo parameter window and connects the values to the setStereoValues function.
        The stereo parameter window allows the user to adjust the stereo settings.

        Returns:
            None
        """

        # Pass the current eye angle
        self.stereo_window.value.connect(self.setStereoValues)
        self.stereo_window.setModal(True)  # Make the dialog modal
        self.stereo_window.show()

    def onAboutClicked(self):
        """
        Handles the click event of the about menu button.

        This method opens the about window.

        Returns:
            None
        """

        self.about_window.setModal(True)  # Make the dialog modal
        self.about_window.show()

    def setStereoValues(self, ipd):
        # Get the active camera from the renderer
        camera = self.renderer.GetActiveCamera()

        # Set the inter-pupillary distance (IPD) in degree
        camera.SetEyeAngle(ipd)
        self.current_ipd = ipd
        # Update the window to apply the changes
        self.vtk_widget.GetRenderWindow().Render()

    def onColorButtonClicked(self):
        """
        Opens a color picker and sets the color of the selected actor based on the chosen color.

        Returns:
            None
        """
        color_dialog = QColorDialog(self)
        chosen_color = color_dialog.getColor()

        if chosen_color.isValid():
            selected_index = self.ui.organ_combo.currentIndex()
            selected_surface_actor = self.segmented_surface_actors[selected_index]
            selected_volume_actor = self.segmented_volume_actors[selected_index]
            rgb = chosen_color.redF(), chosen_color.greenF(), chosen_color.blueF()

            # Set color for the surface actor
            selected_surface_actor.GetProperty().SetColor(rgb)

            # Set color for the volume actor
            color_func = vtk.vtkColorTransferFunction()
            color_func.AddRGBPoint(0, 0, 0, 0)
            color_func.AddRGBPoint(255, *rgb)
            selected_volume_actor.GetProperty().SetColor(color_func)

            self.vtk_widget.GetRenderWindow().Render()
            self.ui.color_button.setStyleSheet(
                f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in rgb)}"
            )
            self.colors[selected_index] = rgb

    def onOpacityChanged(self):
        """
        Handles the change event of the opacity slider.

        This method adjusts the opacity of the selected organ based on the value of the opacity slider.
        The opacity is calculated as a percentage of the maximum value of the slider.
        The method updates the opacity of the selected actor and refreshes the window.

        Returns:
            None
        """
        # Adjust opacity for a selected organ
        selected_index = self.ui.organ_combo.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        opacity = self.ui.op_slider.value() / 100

        # Set opacity for the surface actor
        selected_surface_actor.GetProperty().SetOpacity(opacity)

        # Set opacity for the surface actor
        selected_surface_actor.GetProperty().SetOpacity(opacity)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onStereoClicked(self):
        """
        Handles the click event of the stereo button.

        This method toggles stereo rendering based on the state of the stereo button.
        When the button is checked, it enables stereo rendering and displays stereo parameters.
        When the button is unchecked, it disables stereo rendering and hides stereo parameters.
        The method updates the window and applies the changes to the rendering.

        Returns:
            None
        """
        if self.ui.stereo_button.isChecked():
            self.vtk_widget.GetRenderWindow().SetStereoTypeToCrystalEyes()
            self.vtk_widget.GetRenderWindow().StereoRenderOn()
            # Choose stereo parameters
            self.ui.stereo_param_button.setDisabled(False)

        else:
            self.vtk_widget.GetRenderWindow().StereoRenderOff()
            self.ui.stereo_param_button.setDisabled(True)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onComboBoxChanged(self):
        """
        Handles the change event of the combo box.

        This method changes the selected organ based on the current index of the combo box.
        It updates the opacity slider position based on the opacity of the selected actor.
        The method triggers the corresponding actions for the glass button and volume button.

        Returns:
            None
        """
        # Change organ
        selected_index = self.ui.organ_combo.currentIndex()
        selected_actor = self.segmented_actors[selected_index]

        if isinstance(selected_actor, vtk.vtkActor):
            opacity = selected_actor.GetProperty().GetOpacity()
            self.ui.op_slider.setValue(int(opacity * 100))

        # Update the active color widget with the color of the selected organ
        rgb = tuple(
            int(c * 255) for c in self.colors[selected_index % len(self.colors)]
        )
        self.ui.color_button.setStyleSheet(f"border: 0px; background-color: rgb{rgb};")

        self.onGlassButtonClicked()
        self.onVolumeButtonClicked()

        # Update the histogram
        new_histogram_canvas = self.create_histogram(self.segmented_organs_data)

        # Remove the old histogram canvas
        while self.ui.hist_layout.count():
            child = self.ui.hist_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Add the new histogram canvas to the layout
        self.ui.hist_layout.addWidget(new_histogram_canvas)
        self.ui.low_slider.setValue(0)
        self.ui.high_slider.setValue(255)
        self.ui.high_op_slider.setValue(100)

        # Update volume and surface values
        volume, surface = self.calculate_volume_surface()

        self.ui.volume_value.setText(f"{volume:,.2f} mm³")
        self.ui.surface_value.setText(f"{surface:,.2f} mm²")

    def onGlassButtonClicked(self):
        """
        Handles the click event of the glass button.

        This method toggles between different views based on the state of the glass button.
        When the button is checked, the view changes and volume rendering possibility appears.
        When the button is unchecked, volume rendering disappears and the volume becomes a surface.
        The method updates the visibility of the volume button and triggers the corresponding actions.

        Returns:
            None
        """
        if self.ui.glass_button.isChecked():
            # The view changes
            selected_index = self.ui.organ_combo.currentIndex()

            timer_call = TimerCallback(
                self.segmented_actors, selected_index, self.renderer.GetActiveCamera()
            )
            self.interactor.AddObserver("TimerEvent", timer_call.execute)
            self.interactor.CreateRepeatingTimer(10)

            # Volume rendering possibility appears
            self.ui.hist_group.setDisabled(True)
            self.ui.volume_button.setDisabled(False)
            self.ui.organ_combo.setDisabled(True)
            self.ui.op_slider.setDisabled(True)
        else:
            # Volume rendering disappears and the volume becomes a surface
            self.ui.volume_button.setChecked(False)
            self.ui.volume_button.setDisabled(True)
            self.ui.organ_combo.setDisabled(False)
            self.ui.op_slider.setDisabled(False)
            self.onVolumeButtonClicked()

            # Focal point goes back to normal and all organs have an opacity of 1
            self.renderer.GetActiveCamera().SetFocalPoint(self.default_focal)
            for actor in self.segmented_actors:
                actor.GetProperty().SetOpacity(1)

    def onVolumeButtonClicked(self):
        """
        Handles the click event of the volume button.

        This method toggles between volume rendering and surface rendering based on the state of the volume button.
        When the button is checked, it launches volume rendering of the selected organ. When the button is unchecked,
        it launches surface rendering. The method updates the actors in the renderer accordingly and refreshes the
        window.

        Returns:
            None
        """
        # Delete existing actor of the renderer
        self.renderer.RemoveAllViewProps()
        if self.ui.volume_button.isChecked():
            # If the button is checked: launch volume rendering of the selected organ
            selected_index = self.ui.organ_combo.currentIndex()
            self.segmented_actors = list(self.segmented_surface_actors)
            self.segmented_actors[selected_index] = self.segmented_volume_actors[
                selected_index
            ]
            self.ui.hist_group.setDisabled(False)
            self.ui.measure_tab.setDisabled(True)
        else:
            # If the button is unchecked: launch surface rendering
            self.segmented_actors = list(self.segmented_surface_actors)
            self.ui.hist_group.setDisabled(True)
            self.ui.measure_tab.setDisabled(False)
            for actor in self.selected_cells:
                self.renderer.AddActor(actor)

            for actor in self.line_btw_cells:
                self.renderer.AddActor(actor)

        # Add the actors to the renderer
        for actor in self.segmented_actors:
            self.renderer.AddActor(actor)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def createListSegmentedOrgans(self):
        """
        Creates a list of segmented organs.

        Returns:
            list: A list of vtk data containing each organ. Used for both surface and volume rendering.
        """

        organs = []
        organs_data = []
        for label in self.checked_labels:  # iterate over labels_keys
            organ_data = self.img_data.copy()
            organ_data[
                self.labels_data
                != get_index_from_key(
                    label, get_abs_path("resources/config/labels.yml")
                )
            ] = 0  # Select only the organ with the specific label
            organs_data.append(organ_data)

            # Convert the numpy array to VTK image data
            vtk_organ_data = vtk.vtkImageData()
            vtk_organ_data.SetDimensions(self.img_data.shape)
            vtk_organ_data.SetSpacing(self.img_nii.header.get_zooms())
            vtk_organ_data.AllocateScalars(vtk.VTK_FLOAT, 1)

            # Copy the numpy array to the VTK image data
            vtk_array = numpy_to_vtk(organ_data.flatten("F"), deep=True)

            vtk_organ_data.GetPointData().SetScalars(vtk_array)
            organs.append(vtk_organ_data)
        return organs_data, organs

    def createSegmentedSurfaceActors(self):
        """
        Creates surface actors for segmented organs.

        Returns:
            list: A list of actors. For each organ, create a surface actor from the segmentation data and the CT scan.
        """

        actors = []
        for organ in range(len(self.checked_labels)):
            # Filter data
            cast_filter = vtk.vtkImageCast()
            cast_filter.SetInputData(self.segmented_organs[organ])
            cast_filter.SetOutputScalarTypeToUnsignedShort()

            # Contour mapper : marching cubes
            contour = vtk.vtkMarchingCubes()
            contour.SetInputConnection(cast_filter.GetOutputPort())
            contour.ComputeNormalsOn()
            contour.ComputeGradientsOn()
            contour.SetValue(0, 60)

            con_mapper = vtk.vtkPolyDataMapper()
            con_mapper.SetInputConnection(contour.GetOutputPort())

            # Deactivate the scalar color to redefine a new color
            con_mapper.ScalarVisibilityOff()

            # Set up the surface actor
            surface_actor = vtk.vtkActor()
            surface_actor.SetMapper(con_mapper)

            # Change the color of the surface : to modify to better visualize ...
            # surface_actor.GetProperty().SetAmbientColor(1.0, 0.0, 0.0)  # Couleur ambient rouge (R, G, B)
            # surface_actor.GetProperty().SetDiffuseColor(1.0, 0.0, 0.0)  # Couleur diffuse rouge (R, G, B)
            # surface_actor.GetProperty().SetSpecularColor(1.0, 0.0, 0.0)  # Couleur specular rouge (R, G, B)
            # surface_actor.GetProperty().SetColor(1.0, 0.0, 0.0)  # Red (R, G, B)

            # By default: one color per organ
            color = self.colors[organ % len(self.colors)]
            surface_actor.GetProperty().SetColor(color)

            surface_actor.GetProperty().SetOpacity(1.0)
            actors.append(surface_actor)

        return actors

    def createSegmentedVolumeActors(self):
        """
        Creates volume actors for segmented organs.

        Returns:
            list: A list of actors. For each organ, create a volume actor from the segmentation data and the CT scan.
        """

        actors = []
        # For each organ, create an actor from the segmentation data and the CT scan
        for organ in range(len(self.checked_labels)):
            volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
            volume_mapper.SetInputData(self.segmented_organs[organ])

            # Create a VTK volume property and set the transfer function
            volume_property = vtk.vtkVolumeProperty()
            volume_property.ShadeOn()
            volume_property.SetInterpolationTypeToLinear()

            # Create a VTK color transfer function
            color_func = vtk.vtkColorTransferFunction()
            color = self.colors[
                organ % len(self.colors)
            ]  # Get the color of the corresponding surface actor
            color_func.AddRGBPoint(0, 0, 0, 0)
            color_func.AddRGBPoint(255, *color)
            volume_property.SetColor(color_func)

            # Create a VTK volume gradient opacity function
            opacity_func = vtk.vtkPiecewiseFunction()
            opacity_func.AddPoint(0, 0)
            opacity_func.AddPoint(255, 1)
            volume_property.SetScalarOpacity(opacity_func)

            # Create a VTK volume
            volume_actor = vtk.vtkVolume()
            volume_actor.SetMapper(volume_mapper)
            volume_actor.SetProperty(volume_property)

            actors.append(volume_actor)

        return actors
