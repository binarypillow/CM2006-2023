import vtk
from vtkmodules.util.numpy_support import numpy_to_vtk
from app.utils import get_index_from_key, get_abs_path


def create_list_segmented_organs(self):
    """Creates a list of segmented organs based on the checked labels."""

    organs_data = []
    organs_vtk = []
    for label in self.checked_labels:  # iterate over labels_keys
        organ_data = self.img_data.copy()
        organ_data[
            self.labels_data
            != get_index_from_key(label, get_abs_path("/resources/config/labels.yml"))
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
        organs_vtk.append(vtk_organ_data)
    return organs_data, organs_vtk
