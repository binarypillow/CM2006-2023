import vtk


def calculate_surface_volume(self):
    """
    Calculates the surface area and volume of the selected organ.

    Args:
        self: The instance of the class.

    Returns:
        tuple: A tuple containing the surface area and volume of the selected organ.
    """

    # Get the index of current organ
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

    return mass_properties.GetSurfaceArea(), mass_properties.GetVolume()
