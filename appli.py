from PyQt5 import QtWidgets, uic, QtCore
import sys
import vtk
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from random import random
import nibabel as nib
from vtkmodules.util.numpy_support import numpy_to_vtk

# Visualize less organs instead of 13, so it is faster
global nb_organs
nb_organs = 5


class StereoParam(QtWidgets.QDialog):
    # Signal sent to the first window with the values of IPD and angle
    values = QtCore.pyqtSignal(float, float)

    def __init__(self):
        super(StereoParam, self).__init__()
        self.setWindowTitle('Stereo parameters')
        uic.loadUi('stereo.ui', self)

        self.ipd_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        self.angle_line_edit.textChanged.connect(self.updateOKButtonVisibility)
        self.ok_button.setVisible(False)
        self.ok_button.clicked.connect(self.sendValues)

    def updateOKButtonVisibility(self):
        # Check if the two LineEdits contain numbers
        ipd_text = self.ipd_line_edit.text()
        angle_text = self.angle_line_edit.text()

        try:
            ipd_value = float(ipd_text)
            angle_value = float(angle_text)
            self.ok_button.setVisible(True)
        except ValueError:
            self.ok_button.setVisible(False)

    def sendValues(self):
        ipd_text = self.ipd_line_edit.text()
        angle_text = self.angle_line_edit.text()
        self.values.emit(float(ipd_text), float(angle_text))


class WelcomeWindow(QtWidgets.QDialog):

    def __init__(self):
        super(WelcomeWindow, self).__init__()
        uic.loadUi('welcome.ui', self)
        self.setWindowTitle('File choice')
        self.continue_button.setVisible(False)
        self.img_button.clicked.connect(self.select_image_file)
        self.seg_button.clicked.connect(self.select_segmentation_file)

        self.img_path = ""
        self.label_path = ""
        self.next_window = None

        # Connect the "Continue" button to the function to open a new window
        self.continue_button.clicked.connect(self.open_new_window)

    def select_image_file(self):
        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        # If file is open
        if file_dialog.exec_():
            # Get the path of the selected file
            self.img_path = file_dialog.selectedFiles()[0]
            if self.img_path.endswith(".nii.gz"):
                self.img_box.setChecked(True)
            # Update continue button if both files were selected
            self.check_files()

    def select_segmentation_file(self):

        file_dialog = QtWidgets.QFileDialog()
        file_dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)

        # If file is open
        if file_dialog.exec_():
            # Get the path of the selected file
            self.label_path = file_dialog.selectedFiles()[0]

            if self.label_path.endswith(".nii.gz"):
                self.seg_box.setChecked(True)
            # Update continue button if both files were selected
            self.check_files()

    def check_files(self):
        if self.label_path.endswith(".nii.gz") and self.img_path.endswith(".nii.gz"):
            self.continue_button.setVisible(True)
        else:
            self.continue_button.setVisible(False)

    def open_new_window(self):
        # The next window is the main window
        self.next_window = SecondWindow(self.img_path, self.label_path)
        self.next_window.show()
        self.close()


class SecondWindow(QtWidgets.QMainWindow):
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
            (1.0, 0.81, 0.37)  # Gold
        ]

        super(SecondWindow, self).__init__()
        uic.loadUi('interface.ui', self)

        self.setWindowTitle('Visualization application')
        self.vtk_widget = QVTKRenderWindowInteractor(self.frame)
        self.image_layout.addWidget(self.vtk_widget)

        # Create a list of volume actors : each element in the list is an actor for one organ
        self.segmented_volume_actors = self.createSegmentedVolumeActors()

        # Create a list of surface actors : each element in the list is an actor for one organ
        self.segmented_surface_actors = self.createSegmentedSurfaceActors()

        # Default rendering : surface
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

        # Know the position of the camera each right click : just for us, to better place the camera
        self.interactor.AddObserver('RightButtonPressEvent', self.get_camera_position)

        # Window for stereo parameters
        self.stereo_window = StereoParam()

        # Volume rendering button and stereo parameters are hidden
        self.volume_button.setVisible(False)
        self.stereo_param_button.setVisible(False)

        # Change the actor from surface to volume if volume button is checked
        self.volume_button.setChecked(False)  # initial state : unchecked
        self.volume_button.clicked.connect(self.onVolumeButtonClicked)

        # Slide for opacity change
        self.slider.valueChanged.connect(self.onOpacityChanged)

        # Hide organs not showed in the slider
        while self.comboBox.count() > nb_organs:
            i = self.comboBox.count() - 1
            self.comboBox.removeItem(i)

        # Change the view and show volume rendering if the glass button is clicked
        self.glass_button.clicked.connect(self.onGlassButtonClicked)

        # Change the organ view and volume rendering if user changes the specified organ
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)

        # Display stereo if clicked. Display a parameter button to adjust stereo parameters
        self.stereo_button.clicked.connect(self.onStereoClicked)

        # Choose stereo parameters. It oppens a new dialog window
        self.stereo_param_button.clicked.connect(self.onStereoParamClicked)


    def get_camera_position(self,obj, event):
        # Get the position of the camera at right click mouse to make adjustments for focus mode
        position = self.renderer.GetActiveCamera().GetPosition()
        angle = self.renderer.GetActiveCamera().GetRoll()
        print("Camera's position :", position)
        print("Camera's Roll :", angle)

    def setStereoValues(self, ipd, angle):
        # How do we change the parameters ? Which parameters ?
        print(ipd, angle)

    def onStereoParamClicked(self):
        self.stereo_window.values.connect(self.setStereoValues)
        self.stereo_window.show()

    def onStereoClicked(self):
        if self.stereo_button.isChecked():
            self.vtk_widget.GetRenderWindow().SetStereoTypeToInterlaced()
            self.vtk_widget.GetRenderWindow().StereoRenderOn()
            # Choose stereo parameters
            self.stereo_param_button.setVisible(True)

        else:
            self.vtk_widget.GetRenderWindow().StereoRenderOff()
            self.stereo_param_button.setVisible(False)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onComboBoxChanged(self):
        # Change organ
        selected_index = self.comboBox.currentIndex()
        selected_actor = self.segmented_actors[selected_index]

        # If the actor is a volume, we cannot adjust opacity
        # If the actor is a surface, we must adjust the position of the slider with its opacity
        if isinstance(selected_actor, vtk.vtkActor):
            opacity = selected_actor.GetProperty().GetOpacity()
            self.slider.setValue(int(opacity * 100))

        self.onGlassButtonClicked()
        self.onVolumeButtonClicked()

    def onGlassButtonClicked(self):
        if self.glass_button.isChecked():
            # The view changes and volume rendering possibilitity appear
            print("CHANGE THE VIEW HERE")
            self.volume_button.setVisible(True)
        else:
            # Volume rendering disappear and the volume becomes a surface
            self.volume_button.setChecked(False)
            self.volume_button.setVisible(False)
            self.onVolumeButtonClicked()

    def onOpacityChanged(self, value_slider):
        # Adjust opacitiy for a selected organ
        selected_index = self.comboBox.currentIndex()
        selected_actor = self.segmented_actors[selected_index]
        opacity = value_slider / 100

        if isinstance(selected_actor, vtk.vtkActor):
            selected_actor.GetProperty().SetOpacity(opacity)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def onVolumeButtonClicked(self):
        if self.volume_button.isChecked():
            # If button is checked : launch volume rendering of the selected organ
            selected_index = self.comboBox.currentIndex()
            self.segmented_actors = list(self.segmented_surface_actors)
            self.segmented_actors[selected_index] = self.segmented_volume_actors[selected_index]
            # We cannot adjust opacity for a volume
            self.slider.setVisible(False)

        else:
            # If button is unchecked : launch surface rendering
            self.segmented_actors = list(self.segmented_surface_actors)
            self.slider.setVisible(True)

        # Delete existing actor of the renderer
        self.renderer.RemoveAllViewProps()

        # Add the actors to the renderer
        for actor in self.segmented_actors:
            self.renderer.AddActor(actor)

        # Update window
        self.vtk_widget.GetRenderWindow().Render()

    def createListSegmentedOrgans(self):
        """
        :return: list of vtk data containing each individual organ. Used for both surface and volume rendering
        """
        organs = []
        for label in range(1, nb_organs + 1):  # 13 organs to segment
            organ_data = self.img_data.copy()
            organ_data[self.labels_data != label] = 0  # Select only the organ with the specific label

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

        for organ in range(0, nb_organs):  # 13 organs
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

            # Desactivate the scalar color to redefine a new color
            con_mapper.ScalarVisibilityOff()

            # Set up the surface actor
            surface_actor = vtk.vtkActor()
            surface_actor.SetMapper(con_mapper)

            # Change the color of the surface : to modify to better visualize ...
            # surface_actor.GetProperty().SetAmbientColor(1.0, 0.0, 0.0)  # Couleur ambiante rouge (R, G, B)
            # surface_actor.GetProperty().SetDiffuseColor(1.0, 0.0, 0.0)  # Couleur diffuse rouge (R, G, B)
            # surface_actor.GetProperty().SetSpecularColor(1.0, 0.0, 0.0)  # Couleur spéculaire rouge (R, G, B)
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
        for organ in range(0, nb_organs):  # 13 organs

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


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    # welcome = WelcomeWindow()
    # welcome.show()

    # Use this to display only the second window
    img_path = "data/images/FLARE22_Tr_0001_0000.nii.gz"
    label_path = "data/labels/FLARE22_Tr_0001.nii.gz"

    main_window = SecondWindow(img_path, label_path)
    main_window.show()

    sys.exit(app.exec_())
