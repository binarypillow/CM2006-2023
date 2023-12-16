from PyQt6 import QtWidgets
import vtk
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
import nibabel as nib
from vtkmodules.util.numpy_support import numpy_to_vtk
from app.stereo_dialog import StereoParam
from app.ui import main_interface

# Visualize fewer organs instead of 13, so it is faster
global nb_organs
nb_organs = 5


def setStereoValues(ipd, angle):
    # How do we change the parameters? Which parameters?
    print(ipd, angle)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, path_img, path_label):
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
        self.vtk_widget = QVTKRenderWindowInteractor(self.ui.frame)
        self.ui.image_layout.addWidget(self.vtk_widget)

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
        # INTERACTIONS AND BUTTONS

        # Know the position of the camera each right-click: just for us, to better place the camera
        self.interactor.AddObserver("RightButtonPressEvent", self.get_camera_position)

        # Window for stereo parameters
        self.stereo_window = StereoParam()

        # Volume rendering button and stereo parameters are hidden
        self.ui.volume_button.setVisible(False)
        self.ui.stereo_param_button.setVisible(False)

        # Change the actor from surface to volume if the volume button is checked
        self.ui.volume_button.setChecked(False)  # initial state : unchecked
        self.ui.volume_button.clicked.connect(self.onVolumeButtonClicked)

        # Slide for opacity change
        self.ui.slider.valueChanged.connect(self.onOpacityChanged)

        # Hide organs aren't showed in the slider
        while self.ui.comboBox.count() > nb_organs:
            i = self.ui.comboBox.count() - 1
            self.ui.comboBox.removeItem(i)

        # Change the view and show volume rendering if the glass button is clicked
        self.ui.glass_button.clicked.connect(self.onGlassButtonClicked)

        # Change the organ view and volume rendering if user changes the specified organ
        self.ui.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

        # Display stereo if clicked. Display a parameter button to adjust stereo parameters
        self.ui.stereo_button.clicked.connect(self.onStereoClicked)

        # Choose stereo parameters. It opens a new dialog window
        self.ui.stereo_param_button.clicked.connect(self.onStereoParamClicked)

    def get_camera_position(self, obj, event):
        # Get the position of the camera at right click mouse to make adjustments for focus mode
        position = self.renderer.GetActiveCamera().GetPosition()
        angle = self.renderer.GetActiveCamera().GetRoll()
        print("Camera's position :", position)
        print("Camera's Roll :", angle)

    def onStereoParamClicked(self):
        self.stereo_window.values.connect(setStereoValues)
        self.stereo_window.show()

    def onStereoClicked(self):
        if self.ui.stereo_button.isChecked():
            self.vtk_widget.GetRenderWindow().SetStereoTypeToInterlaced()
            self.vtk_widget.GetRenderWindow().StereoRenderOn()
            # Choose stereo parameters
            self.ui.stereo_param_button.setVisible(True)

        else:
            self.vtk_widget.GetRenderWindow().StereoRenderOff()
            self.ui.stereo_param_button.setVisible(False)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onComboBoxChanged(self):
        # Change organ
        selected_index = self.ui.comboBox.currentIndex()
        selected_actor = self.segmented_actors[selected_index]

        # If the actor is a volume, we cannot adjust opacity
        # If the actor is a surface, we must adjust the position of the slider with its opacity
        if isinstance(selected_actor, vtk.vtkActor):
            opacity = selected_actor.GetProperty().GetOpacity()
            self.ui.slider.setValue(int(opacity * 100))

        self.onGlassButtonClicked()
        self.onVolumeButtonClicked()

    def onGlassButtonClicked(self):
        if self.ui.glass_button.isChecked():
            # The view changes and volume rendering possibility appear
            print("CHANGE THE VIEW HERE")
            self.ui.volume_button.setVisible(True)
        else:
            # Volume rendering disappears and the volume becomes a surface
            self.ui.volume_button.setChecked(False)
            self.ui.volume_button.setVisible(False)
            self.onVolumeButtonClicked()

    def onOpacityChanged(self, value_slider):
        # Adjust opacity for a selected organ
        selected_index = self.ui.comboBox.currentIndex()
        selected_actor = self.segmented_actors[selected_index]
        opacity = value_slider / 100

        if isinstance(selected_actor, vtk.vtkActor):
            selected_actor.GetProperty().SetOpacity(opacity)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onVolumeButtonClicked(self):
        if self.ui.volume_button.isChecked():
            # If the button is checked: launch volume rendering of the selected organ
            selected_index = self.ui.comboBox.currentIndex()
            self.segmented_actors = list(self.segmented_surface_actors)
            self.segmented_actors[selected_index] = self.segmented_volume_actors[
                selected_index
            ]
            # We cannot adjust opacity for a volume
            self.ui.slider.setVisible(False)

        else:
            # If the button is unchecked: launch surface rendering
            self.segmented_actors = list(self.segmented_surface_actors)
            self.ui.slider.setVisible(True)

        # Delete existing actor of the renderer
        self.renderer.RemoveAllViewProps()

        # Add the actors to the renderer
        for actor in self.segmented_actors:
            self.renderer.AddActor(actor)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def createListSegmentedOrgans(self):
        """
        :return: list of vtk data containing each organ. Used for both surface and volume rendering
        """
        organs = []
        for label in range(1, nb_organs + 1):  # 13 organs to segment
            organ_data = self.img_data.copy()
            organ_data[
                self.labels_data != label
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
        :return: list of actors. For each organ, create a surface actor from the segmentation data and the CT scan
        """

        actors = []

        for organ in range(nb_organs):  # 13 organs
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

            # By default : one color per organ
            color = self.colors[organ % len(self.colors)]
            surface_actor.GetProperty().SetColor(color)

            surface_actor.GetProperty().SetOpacity(1.0)
            actors.append(surface_actor)

        return actors

    def createSegmentedVolumeActors(self):
        """
        :return: list of actors. For each organ, create a volume actor from the segmentation data and the CT scan
        """
        actors = []
        # For each organ, create an actor from the segmentation data and the CT scan
        for organ in range(nb_organs):  # 13 organs
            volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
            volume_mapper.SetInputData(self.segmented_organs[organ])

            # Create a VTK volume property and set the transfer function
            volume_property = vtk.vtkVolumeProperty()
            volume_property.ShadeOn()
            volume_property.SetInterpolationTypeToLinear()

            # Create a VTK color transfer function
            color_func = vtk.vtkColorTransferFunction()
            color_func.AddRGBPoint(0, 0, 0, 0)
            color_func.AddRGBPoint(255, 1, 1, 1)
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
