"""
Little demo file to demonstrate how to visualize a single organ (the liver).
"""

import nibabel as nib
import vtkmodules.all as vtk
from vtkmodules.util.numpy_support import numpy_to_vtk

# Load the nii.gz file with the images
img_nii = nib.load("data/images/FLARE22_Tr_0001_0000.nii.gz")
img_data = img_nii.get_fdata()

# Load the nii.gz file with the labels
labels_nii = nib.load("data/labels/FLARE22_Tr_0001.nii.gz")
labels_data = labels_nii.get_fdata()

# Select only the segmentation of the liver
liver = img_data.copy()
liver[labels_data != 1] = 0

# Convert the numpy array to VTK image data
vtk_data = vtk.vtkImageData()
vtk_data.SetDimensions(img_data.shape)
vtk_data.SetSpacing(img_nii.header.get_zooms())
vtk_data.AllocateScalars(vtk.VTK_FLOAT, 1)

# Copy the numpy array to the VTK image data
vtk_array = numpy_to_vtk(liver.flatten("F"), deep=True)
vtk_data.GetPointData().SetScalars(vtk_array)

# Create a VTK renderer, render window, and interactor
renderer = vtk.vtkRenderer()
render_window = vtk.vtkRenderWindow()
render_window.AddRenderer(renderer)
interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create a VTK volume and mapper
volume_mapper = vtk.vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputData(vtk_data)

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
volume = vtk.vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Add the volume to the renderer and set the background color
renderer.AddVolume(volume)
renderer.SetBackground(1, 1, 1)  # White background

# Set up the camera and start the interactor
renderer.ResetCamera()
render_window.Render()
interactor.Start()
