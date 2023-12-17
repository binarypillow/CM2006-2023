from PyQt6 import QtWidgets
from PyQt6.QtWidgets import QColorDialog
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import nibabel as nib
from vtkmodules.util.numpy_support import numpy_to_vtk
from app.stereo_dialog import StereoParam
from app.ui import main_interface
from app.utils import get_index_from_key, get_abs_path


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
        self.segmented_organs = self.createListSegmentedOrgans()

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
        self.interactor.Start()

        ##############################################################################################
        # MENU TOOLS BAR

        # Exit menu button
        self.ui.actionClose.triggered.connect(self.close)

        ##############################################################################################
        # INTERACTIONS AND BUTTONS

        # Initialize color
        self.ui.color_button.setStyleSheet(
            f"border: 0px; background-color: rgb{tuple(int(c * 255) for c in self.colors[0])}"
        )

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
            self.ui.comboBox.addItem(organ)

        # Change the view and show volume rendering if the glass button is clicked
        self.ui.glass_button.clicked.connect(self.onGlassButtonClicked)
        self.ui.color_button.clicked.connect(self.onColorButtonClicked)

        # Change the organ view and volume rendering if user changes the specified organ
        self.ui.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

        # Display stereo if clicked. Display a parameter button to adjust stereo parameters
        self.ui.stereo_button.clicked.connect(self.onStereoClicked)

        # Choose stereo parameters. It opens a new dialog window
        self.ui.stereo_param_button.clicked.connect(self.onStereoParamClicked)

        self.ui.actionClose.triggered.connect(self.close)

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
            selected_index = self.ui.comboBox.currentIndex()
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

    def onOpacityChanged(self, value_slider):
        """
        Handles the change event of the opacity slider.

        This method adjusts the opacity of the selected organ based on the value of the opacity slider.
        The opacity is calculated as a percentage of the maximum value of the slider.
        The method updates the opacity of the selected actor and refreshes the window.

        Args:
            value_slider (int): The value of the opacity slider.

        Returns:
            None
        """
        # Adjust opacity for a selected organ
        selected_index = self.ui.comboBox.currentIndex()
        selected_surface_actor = self.segmented_surface_actors[selected_index]
        selected_volume_actor = self.segmented_volume_actors[selected_index]
        opacity = value_slider / 100 + 0.01

        # Set opacity for the surface actor
        selected_surface_actor.GetProperty().SetOpacity(opacity)

        # Set opacity for the volume actor
        opacity_func = vtk.vtkPiecewiseFunction()
        opacity_func.AddPoint(0, 0)
        opacity_func.AddPoint(255, opacity)
        selected_volume_actor.GetProperty().SetScalarOpacity(opacity_func)

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
        selected_index = self.ui.comboBox.currentIndex()
        selected_actor = self.segmented_actors[selected_index]

        # If the actor is a volume, we cannot adjust opacity
        # If the actor is a surface, we must adjust the position of the slider with its opacity
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
            # The view changes and volume rendering possibility appear
            print("CHANGE THE VIEW HERE")
            self.ui.volume_button.setDisabled(False)
            self.ui.comboBox.setDisabled(True)
        else:
            # Volume rendering disappears and the volume becomes a surface
            self.ui.volume_button.setChecked(False)
            self.ui.volume_button.setDisabled(True)
            self.ui.comboBox.setDisabled(False)
            self.onVolumeButtonClicked()

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
        if self.ui.volume_button.isChecked():
            # If the button is checked: launch volume rendering of the selected organ
            selected_index = self.ui.comboBox.currentIndex()
            self.segmented_actors = list(self.segmented_surface_actors)
            self.segmented_actors[selected_index] = self.segmented_volume_actors[
                selected_index
            ]
        else:
            # If the button is unchecked: launch surface rendering
            self.segmented_actors = list(self.segmented_surface_actors)

        # Delete existing actor of the renderer
        self.renderer.RemoveAllViewProps()

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
        for label in self.checked_labels:  # iterate over labels_keys
            organ_data = self.img_data.copy()
            organ_data[
                self.labels_data
                != get_index_from_key(
                    label, get_abs_path("resources/config/labels.yml")
                )
            ] = 0  # Select only the organ with the specific label

            # Convert the numpy array to VTK image data
            vtk_organ_data = vtk.vtkImageData()
            vtk_organ_data.SetDimensions(self.img_data.shape)
            vtk_organ_data.SetSpacing(self.img_nii.header.get_zooms())
            vtk_organ_data.AllocateScalars(vtk.VTK_FLOAT, 1)

            # Copy the numpy array to the VTK image data
            vtk_array = numpy_to_vtk(organ_data.flatten("F"), deep=True)
            vtk_organ_data.GetPointData().SetScalars(vtk_array)
            organs.append(vtk_organ_data)
        return organs

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
            contour.SetValue(0, 100)

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
