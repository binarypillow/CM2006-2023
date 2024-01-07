from PyQt6 import QtWidgets
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import nibabel as nib
from app.stereo_dialog import StereoParam
from app.about_dialog import AboutText
from app.ui import main_interface
from app.main_window.callback import TimerCallback, TimerChangeView


class MainWindow(QtWidgets.QMainWindow):
    """Main window for the visualisation application."""

    def __init__(self, path_img, path_label, checked_labels):
        # ---- Variables initialization ----
        # Load the nii.gz file with the images
        self.img_nii = nib.load(path_img)
        self.img_data = self.img_nii.get_fdata()
        # Load the nii.gz file with the segmentation labels
        labels_nii = nib.load(path_label)
        self.labels_data = labels_nii.get_fdata()

        # Set the colours for surface organs
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
        # Store checked labels
        self.checked_labels = checked_labels

        # ---- Interface initialization ----
        super(MainWindow, self).__init__()
        self.ui = main_interface.Ui_MainWindow()
        self.ui.setupUi(self)

        # ---- VTK ACTORS
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.render_frame)
        self.ui.vtk_frame.addWidget(self.vtk_widget)

        # Create a list containing each organ separated
        (
            self.segmented_organs_data,
            self.segmented_organs,
        ) = self.create_list_segmented_organs()
        # Create a list of volume actors: each element in the list is an actor for one organ
        self.segmented_volume_actors = self.create_segmented_volume_actors()

        # Create a list of surface actors: each element in the list is an actor for one organ
        self.segmented_surface_actors = self.create_segmented_surface_actors()

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

        # Set interactor, initialise and start
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.Initialize()

        # Store the initial camera settings
        self.initial_camera_position = self.renderer.GetActiveCamera().GetPosition()
        self.initial_camera_roll = self.renderer.GetActiveCamera().GetRoll()
        self.initial_camera_focal_point = (
            self.renderer.GetActiveCamera().GetFocalPoint()
        )

        # ---- MENU TOOL BAR
        # About
        self.about_window = AboutText()
        self.ui.actionInfo.triggered.connect(self.on_about_clicked)
        # Load new
        self.ui.actionLoad.triggered.connect(self.on_load_clicked)
        # Close
        self.ui.actionClose.triggered.connect(self.close)
        # Reset view
        self.ui.actionReset_view.triggered.connect(self.reset_view)
        # View
        for action in self.ui.menuChange_view.actions():
            action.triggered.connect(self.on_action_view)

        # ---- ORGAN SELECTION
        for organ in self.checked_labels:  # Create the comboBox list
            self.ui.organ_combo.addItem(organ)
        self.ui.color_button.setStyleSheet(
            f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in self.colors[0])}"
        )
        # Connect the Color button to the function to change the color of the selected organ
        self.ui.color_button.clicked.connect(self.on_color_button)
        # Change the organ view and volume rendering if user changes the specified organ
        self.ui.organ_combo.currentIndexChanged.connect(self.on_combo_box_changed)
        # Connect the opacity slider to the function to change the opacity of the selected organ
        self.ui.op_slider.valueChanged.connect(self.on_opacity_changed)
        # Connect the "Glass" button to the function to change the view and enable the volume
        # rendering option
        self.ui.glass_button.clicked.connect(self.on_glass_button_clicked)
        # Get the current focal point (for the animation)
        self.default_focal = self.renderer.GetActiveCamera().GetFocalPoint()

        # ---- VOLUME RENDERING
        # Change the actor from surface to volume if the volume button is checked
        self.ui.volume_button.setChecked(False)  # initial state: unchecked
        # Connect the button to the activate volume rendering for the selected organ
        self.ui.volume_button.clicked.connect(self.on_volume_button_clicked)
        # Create the histogram for the selected organ
        histogram_canvas = self.create_histogram(self.segmented_organs_data)
        # Draw the histogram
        self.ui.hist_layout.addWidget(histogram_canvas)
        # Slider to control the opacity function points
        self.ui.low_slider.valueChanged.connect(self.on_hist_slider_changed)
        self.ui.high_slider.valueChanged.connect(self.on_hist_slider_changed)
        self.ui.high_op_slider.valueChanged.connect(self.on_hist_slider_changed)
        # Connect the "Update" button to the function to update the rendering window
        self.ui.update_button.clicked.connect(self.on_volume_update)

        # ---- STEREO RENDERING
        # Display stereo if clicked. Display a parameter button to adjust stereo parameters
        self.ui.stereo_button.clicked.connect(self.on_stereo_clicked)
        # Choose stereo parameters. It opens a new dialog window
        self.ui.stereo_param_button.clicked.connect(self.on_stereo_param_clicked)
        # Window for stereo parameters
        self.current_ipd = self.renderer.GetActiveCamera().GetEyeSeparation()
        self.stereo_window = StereoParam(self.current_ipd)

        # ---- RULERS
        self.selected_cells = []
        self.selected_cell_positions = []
        self.line_btw_cells = []
        # Dict in which the visible states of the items will be saved: False = Visible, True = Hidden
        self.item_states = {}

        # Observer's ID used to track left mouse clicks during the creation of a ruler
        self.left_button_observer_id = 0
        # Initial state of the ruler button: False = Not clicked yet
        self.newruler_state = False
        # Connect the "New ruler" button to the function to add a new ruler in the scene
        self.ui.newruler_button.clicked.connect(self.activate_left_click_event)
        # Create a cell picker
        self.cell_picker = vtk.vtkCellPicker()
        # Set the tolerance for picking a point
        self.cell_picker.SetTolerance(0.0005)
        self.interactor.Start()

        # ---- MEASURES
        # Calculate the surface area and the volume of the selected organ
        volume, area = self.calculate_surface_volume()
        # Set the values
        self.ui.surface_value.setText(f"{area:,.2f} mm²")
        self.ui.volume_value.setText(f"{volume:,.2f} mm³")

        # ---- DEBUG
        # The position of the camera each right-click: just for us, to better place the camera
        # self.interactor.AddObserver("RightButtonPressEvent", self.get_camera_position)

        # ---- LABELS
        self.ui.labels_button.clicked.connect(self.on_labels_button_clicked)
        self.arrows = self.create_arrow_text()
        for arrow, text in self.arrows:
            self.renderer.AddActor(arrow)
            self.renderer.AddActor(text)

        self.interactor.AddObserver(vtk.vtkCommand.ModifiedEvent, self.on_camera_change)

    # ---- Methods imports ----
    # ---- VTK
    from ._surfaceactors import create_segmented_surface_actors
    from ._volumeactors import create_segmented_volume_actors
    from ._createlist import create_list_segmented_organs

    # ---- ORGAN SELECTION
    from ._focusandcamera import on_glass_button_clicked, on_action_view, reset_view
    from ._combochange import on_combo_box_changed
    from ._colorselection import on_color_button
    from ._opacitychange import on_opacity_changed

    # ---- VOLUME RENDERING
    from ._volumerendering import on_volume_button_clicked, on_volume_update
    from ._histogram import create_histogram, on_hist_slider_changed

    # --- STEREO RENDERING
    from ._stereorender import set_stereo_values, on_stereo_clicked

    # ---- RULERS
    from ._rulers import (
        activate_left_click_event,
        on_left_button_press,
        add_item_with_buttons,
        hide_item,
        delete_item,
    )

    # ---- MEASURES
    from ._measures import calculate_surface_volume

    # ---- LABELS
    from ._labels import (
        on_labels_button_clicked,
        create_arrow_text,
        update_arrow_and_text,
        on_camera_change,
    )

    def on_stereo_param_clicked(self):
        """
        Opens the stereo parameter dialogue and connects the value signal to the set_stereo_values method.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        # Pass the current eye angle
        self.stereo_window.value.connect(self.set_stereo_values)
        self.stereo_window.setModal(True)  # Make the dialogue modal
        self.stereo_window.show()

    def on_about_clicked(self):
        """
        Opens the "about" window as a modal dialogue.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        self.about_window.setModal(True)  # Make the dialogue modal
        self.about_window.show()  # Show the window

    def on_load_clicked(self):
        """
        Handles the click event of the load button.

        Args:
            self: The instance of the class.

        Returns:
            None
        """

        self.close()  # Close the current window

        # Import here to avoid circular import error
        from app.welcome_window import WelcomeWindow

        welcome_window = WelcomeWindow()
        welcome_window.show()  # Show "welcome" window

    # ---- DEBUG
    def get_camera_position(self, obj, event):
        """
        Gets the position, roll angle, and focal point of the camera at the right-click mouse event.

        Args:
            self: The instance of the class.
            obj: The object associated with the event.
            event: The event that triggered the function.

        Returns:
            None
        """

        # Get the position of the camera at right click mouse to make adjustments for focus mode
        position = self.renderer.GetActiveCamera().GetPosition()
        angle = self.renderer.GetActiveCamera().GetRoll()
        focal = self.renderer.GetActiveCamera().GetFocalPoint()
        print("Camera's position :", position)
        print("Camera's Roll :", angle)
        print("Camera's Focal point :", focal)
