import vtk


def create_segmented_volume_actors(self):
    """
    Create segmented volume actors for each checked label.

    Args:
        self: The instance of the class.

    Returns:
        list: A list of vtkVolume objects representing the segmented volume actors.
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
